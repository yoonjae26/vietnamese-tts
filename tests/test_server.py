import io
import urllib.parse

import numpy as np
import pytest

pytest.importorskip("fastapi")
sf = pytest.importorskip("soundfile")
from fastapi.testclient import TestClient  # noqa: E402

from vitts.server import Audio, BackendError, create_app, decode_wav, parse_workers  # noqa: E402


class FakeBackend:
    def __init__(self, name, sample_rate=16000, fail=False):
        self.info = {"engine": name, "name": f"Fake {name}", "license": "MIT", "sample_rate": sample_rate}
        self.calls = []
        self.fail = fail

    def synthesize(self, text, seed):
        if self.fail:
            raise BackendError("worker chết")
        self.calls.append((text, seed))
        return Audio(np.full(1600, 0.1, dtype=np.float32), self.info["sample_rate"])


@pytest.fixture
def backends():
    return {"f5": FakeBackend("f5", 24000), "mms": FakeBackend("mms"), "down": FakeBackend("down", fail=True)}


@pytest.fixture
def client(backends):
    return TestClient(create_app(backends, default_model="f5"))


def test_models_lists_all_backends(client):
    ids = [m["id"] for m in client.get("/v1/models").json()["data"]]
    assert ids == ["f5", "mms", "down"]


def test_routes_by_model_and_normalizes(client, backends):
    r = client.post("/v1/audio/speech", json={"model": "mms", "input": "Giá 100k."})
    assert r.status_code == 200
    assert r.headers["x-model"] == "mms"
    assert backends["mms"].calls == [("giá một trăm nghìn.", 1234)]
    assert urllib.parse.unquote(r.headers["x-normalized-text"]) == "giá một trăm nghìn."
    data, sr = sf.read(io.BytesIO(r.content))
    assert sr == 16000 and len(data) == 1600


def test_openai_default_model_name_maps_to_default(client, backends):
    r = client.post("/v1/audio/speech", json={"model": "tts-1", "input": "xin chào", "voice": "alloy"})
    assert r.headers["x-model"] == "f5"
    assert backends["f5"].calls


def test_long_text_is_split_and_joined_with_pause(client, backends):
    text = "Câu một. Câu hai."
    r = client.post("/v1/audio/speech", json={"model": "f5", "input": text, "response_format": "pcm"})
    assert [c[0] for c in backends["f5"].calls] == ["câu một.", "câu hai."]
    pause = int(24000 * 0.15)
    assert len(r.content) == (1600 * 2 + pause) * 2


def test_errors(client):
    assert client.post("/v1/audio/speech", json={"model": "nope", "input": "a"}).status_code == 404
    assert client.post("/v1/audio/speech", json={"model": "down", "input": "a"}).status_code == 502
    assert client.post("/v1/audio/speech", json={"input": ""}).status_code == 422
    assert client.post("/v1/audio/speech", json={"input": "a", "response_format": "ogg"}).status_code == 422


def test_normalize_endpoint(client):
    assert client.post("/v1/normalize", json={"input": "100k"}).json() == {"text": "một trăm nghìn"}


def test_decode_wav_roundtrip():
    buf = io.BytesIO()
    sf.write(buf, np.array([0.0, 0.5, -0.5], dtype=np.float32), 22050, format="WAV", subtype="PCM_16")
    audio = decode_wav(buf.getvalue())
    assert audio.sample_rate == 22050
    assert np.allclose(audio.samples, [0, 0.5, -0.5], atol=1e-3)


def test_parse_workers():
    assert parse_workers(["f5=http://a:1,mms=http://b:2", "x=http://c:3"]) == {
        "f5": "http://a:1",
        "mms": "http://b:2",
        "x": "http://c:3",
    }
    with pytest.raises(SystemExit):
        parse_workers(["f5"])
