import pytest

torch = pytest.importorskip("torch")

from vitts.translit.model import EOS, Config, Seq2Seq, Vocab, load, save  # noqa: E402


def test_vocab_roundtrip():
    v = Vocab(list("công tê nơ"))
    ids = v.encode("công tê nơ")
    assert ids[0] == 1 and ids[-1] == EOS
    assert v.decode(ids[1:]) == "công tê nơ"


def test_model_shapes_and_save_load(tmp_path):
    src, tgt = Vocab(list("abc")), Vocab(list("xyz "))
    model = Seq2Seq(Config(d_model=32, nhead=2, enc_layers=1, dec_layers=1, ff=64), len(src), len(tgt)).eval()
    s = torch.tensor([src.encode("abc")])
    logits = model(s, torch.tensor([tgt.encode("xy")[:-1]]))
    assert logits.shape == (1, 3, len(tgt))
    assert model.greedy(s, max_len=5).shape[0] == 1
    assert isinstance(model.beam(s, width=2, max_len=5), list)

    path = tmp_path / "m.pt"
    save(path, model, src, tgt)
    loaded, src2, tgt2 = load(path)
    assert src2.itos == src.itos and tgt2.itos == tgt.itos
    assert torch.allclose(loaded(s, torch.tensor([[1]])), model(s, torch.tensor([[1]])), atol=1e-2)
