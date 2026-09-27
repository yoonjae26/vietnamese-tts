from vitts.datasets import vi_ljspeech, vi_wav_txt_pairs


def test_vi_ljspeech(tmp_path):
    (tmp_path / "metadata.csv").write_text("a1|Giá 100k|\na2|Xin chào|spk2\nbad-line\n", encoding="utf-8")
    items = vi_ljspeech(str(tmp_path), "metadata.csv")
    assert [i["text"] for i in items] == ["giá một trăm nghìn", "xin chào"]
    assert items[0]["audio_file"].endswith("wavs/a1.wav")
    assert [i["speaker_name"] for i in items] == ["default", "spk2"]


def test_vi_wav_txt_pairs(tmp_path):
    spk = tmp_path / "speaker_a"
    spk.mkdir()
    (spk / "x.wav").write_bytes(b"")
    (spk / "x.txt").write_text("Lúc 7h", encoding="utf-8")
    (spk / "no_text.wav").write_bytes(b"")
    items = vi_wav_txt_pairs(str(tmp_path))
    assert len(items) == 1
    assert items[0]["text"] == "lúc bảy giờ"
    assert items[0]["speaker_name"] == "speaker_a"
