import io

import numpy as np
import pytest

pytest.importorskip("fastapi")
sf = pytest.importorskip("soundfile")
from fastapi.testclient import TestClient  # noqa: E402

from vitts.server import create_app  # noqa: E402
from vitts.synthesizer import Audio  # noqa: E402


class FakeTTS:
    model_name = "fake"
    sample_rate = 16000

    def __init__(self):
        self.calls = []

    def synthesize(self, text, speed=1.0, speaker=None):
        self.calls.append((text, speed, speaker))
        if not text.strip():
            raise ValueError("empty")
        return Audio(np.zeros(1600, dtype=np.float32), self.sample_rate)


@pytest.fixture
def client():
    fake = FakeTTS()
    c = TestClient(create_app(fake))
    c.fake = fake
    return c


def test_health(client):
    assert client.get("/health").json()["model"] == "fake"


def test_speech_wav(client):
    r = client.post("/v1/audio/speech", json={"input": "Xin chào", "voice": "alloy", "speed": 1.2})
    assert r.status_code == 200
    assert r.headers["content-type"] == "audio/wav"
    data, sr = sf.read(io.BytesIO(r.content))
    assert sr == 16000 and len(data) == 1600
    assert client.fake.calls == [("Xin chào", 1.2, None)]


def test_speech_pcm(client):
    r = client.post("/v1/audio/speech", json={"input": "a", "response_format": "pcm"})
    assert len(r.content) == 1600 * 2


def test_speech_validation(client):
    assert client.post("/v1/audio/speech", json={"input": ""}).status_code == 422
    assert client.post("/v1/audio/speech", json={"input": " "}).status_code == 400
    assert client.post("/v1/audio/speech", json={"input": "a", "response_format": "ogg"}).status_code == 422


def test_normalize_endpoint(client):
    assert client.post("/v1/normalize", json={"input": "100k"}).json() == {"text": "một trăm nghìn"}
