# ViTTS-Bench: full results

Every number here is produced by scripts in this repository. Raw outputs are in [`results/`](../results/). Charts are rendered with `python docs/assets/make_charts.py`.

- [TTS models](#tts-models)
- [Text normalization](#text-normalization)
- [Loanword transliteration](#loanword-transliteration)
- [Reproduce](#reproduce)

## TTS models

All seven models are published by other authors (linked below); this repo only benchmarks them.

50 shared sentences, already written as spoken words (no digits or abbreviations), so only the TTS model is measured. [`vinai/PhoWhisper-large`](https://huggingface.co/vinai/PhoWhisper-large) transcribes each clip and WER is computed against the input. Each model uses its authors' recommended settings and a fixed seed. Voice-cloning models all use the same reference: 8 seconds of the repository author's voice, recorded on a phone ([`benchmark/tts/reference/`](../benchmark/tts/reference/)).

| Model | WER ↓ | WER short | WER tongue twisters | Runaway ↓ | Voice similarity ↑ | UTMOS ↑ | RTF ↓ | VRAM | License |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [IndexTTS-2 Vietnamese](https://huggingface.co/dinhthuan/index-tts-2-vietnamese) | **1.8%** | **0.0%** | **12.2%** | 0/50 | **0.741** | 1.99 | 1.063 | 8.9 GB | Apache-2.0\* |
| [F5-TTS-Vietnamese-1000h](https://huggingface.co/hynt/F5-TTS-Vietnamese-ViVoice) | 3.0% | **0.0%** | 14.9% | 0/50 | 0.731 | 2.21 | 0.219 | 0.8 GB | CC-BY-NC-SA-4.0 |
| [VieNeu-TTS v3 Turbo](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) | 3.3% | 6.7% | 18.9% | 0/50 | 0.656 | 2.16 | 0.101 | 0.9 GB | **Apache-2.0** |
| [Piper vi_VN-vais1000-medium](https://huggingface.co/rhasspy/piper-voices) | 5.7% | 4.4% | 39.2% | 0/50 | (0.198) | 2.37 | 0.037 (CPU) | – | CC-BY-4.0 |
| [MMS-TTS (Meta)](https://huggingface.co/facebook/mms-tts-vie) | 6.9% | 11.1% | 28.4% | 0/50 | (0.318) | **2.74** | **0.013** | **0.4 GB** | CC-BY-NC-4.0 |
| [viXTTS](https://huggingface.co/capleaf/viXTTS) | 9.2% | 24.4% | 41.9% | 0/50 | 0.638 | 2.20 | 0.202 | 2.3 GB | CPML (non-commercial) |
| [VietTTS](https://huggingface.co/dangvansam/viet-tts) | 12.0% | 13.3% | 41.9% | 0/50 | 0.728 | 2.39 | 0.395 | 1.7 GB | CC |

RTF is measured on one NVIDIA H200 (Piper on CPU). \* Commercial use requires permission from the IndexTTS authors.

**Metrics**
- **Runaway:** sentences whose seconds-per-word exceed 3× the model's own median, i.e. the model keeps producing silence or noise after the text. ASR ignores trailing silence, so WER cannot see this.
- **Voice similarity:** cosine similarity of [ECAPA-TDNN](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) embeddings of the reference and the generated audio. MMS and Piper do not clone voices; their scores (in brackets) are a different-speaker baseline. `wavlm-base-plus-sv` was tried first and dropped: it gave an unrelated female voice (Piper) 0.94, close to the cloning models, so it mostly separates gender.
- **UTMOS:** predicted naturalness (1 to 5) from [UTMOS22](https://github.com/tarepan/SpeechMOS), trained on English. Cloning models copy the recording conditions of the reference (the phone recording itself scores 1.82), so compare UTMOS only among cloning models.

**Limitations:** ASR-based WER measures intelligibility, not naturalness. Tongue twisters are hard for the ASR too. A human MOS test and recordings of real speakers (to measure the ASR's own error floor) are still missing.

### The reference voice changes the results

The benchmark was run with two references. The first run is archived in [`results/archive/`](../results/archive/).

| | Reference A: viXTTS sample file | Reference B: author's phone recording |
|---|---:|---:|
| IndexTTS-2 runaway sentences | ⚠️ 5/50 | 0/50 |
| viXTTS WER on short sentences | 46.7% | 24.4% |
| viXTTS voice similarity | 0.812 (best) | 0.638 (worst) |
| F5 / VieNeu / IndexTTS-2 WER | 2.3% / 2.8% / 1.9% | 3.0% / 3.3% / 1.8% |
| UTMOS of the reference itself | 2.41 | 1.82 |

- With reference A, IndexTTS-2 read the sentence correctly and then generated about 28 seconds of silence on 5 of 50 sentences. With reference B this never happened.
- viXTTS benefits when the reference comes from its own sample files.
- The ranking of the top three models by WER is stable across both references. A trustworthy voice-cloning benchmark needs several references (male, female, studio, phone).

## Text normalization

**Held-out v2** (60 sentences, [committed before vitts 0.2 was written](../benchmark/normalization/build_testset.py)) is the headline set. Cells show sentences normalized exactly right, with WER in brackets.

| Category | n | vitts 0.2 (rules) | **vitts 0.2 + transliteration** | vinorm 2.0.7 | soe-vinorm 0.3.2 | vietnormalizer 0.2.3 |
|---|---:|---:|---:|---:|---:|---:|
| Loanwords | 18 | 0% (38.1%) | **67% (6.7%)** | 0% (38.1%) | 0% (38.1%) | 61% (8.6%) |
| Foreign names | 7 | 0% (61.1%) | 43% (18.9%) | 0% (61.1%) | 0% (61.1%) | **57% (13.5%)** |
| Acronyms | 12 | 50% (27.1%) | **75% (9.4%)** | 0% (38.8%) | 25% (27.5%) | 50% (25.0%) |
| Numbers | 4 | **100% (0.0%)** | **100% (0.0%)** | 50% (8.0%) | 75% (4.0%) | 25% (20.0%) |
| Units | 4 | **100% (0.0%)** | **100% (0.0%)** | 25% (22.6%) | 50% (6.5%) | 0% (46.4%) |
| Abbreviations | 4 | **100% (0.0%)** | **100% (0.0%)** | **100% (0.0%)** | **100% (0.0%)** | 0% (48.3%) |
| Plain text | 6 | **83% (5.7%)** | **83% (2.9%)** | **83% (5.7%)** | **83% (5.7%)** | **83% (2.9%)** |
| Mixed | 5 | 0% (45.9%) | **20% (11.5%)** | 0% (45.9%) | 0% (45.9%) | **20% (11.5%)** |
| **Total** | 60 | 38% (28.3%) | **70% (7.4%)** | 20% (32.8%) | 28% (29.1%) | 47% (18.6%) |
| ms / sentence | | 0.2 | 296.3 | 30.1 | 0.4 | 0.4 |

- Most of the gain comes from the transliteration model: without it vitts reaches 38%.
- vietnormalizer is better on foreign names thanks to its 17.7k-word dictionary.
- **Seen vs. unseen words:** the transliteration model was trained on vietnormalizer's dictionary, so 32 of the 55 loanwords in v2 appear in its training split. On the 22 sentences whose loanwords are all unseen, vitts scores 64% and vietnormalizer 50%.
- Speed is the weak point: about 300 ms per sentence on CPU when a sentence has many loanwords, because each word is decoded separately.

<details>
<summary>Held-out v1 (59 sentences) and dev (99 sentences)</summary>

| Set | vitts 0.1 | vitts 0.2 | vitts 0.2 + transliteration | vinorm | soe-vinorm | vietnormalizer |
|---|---:|---:|---:|---:|---:|---:|
| Held-out v1 | 59% | 85%\* | 86%\* | 59% | 76% | 44% |
| Dev | 100%\* | 100%\* | 100%\* | 83% | 90% | 66% |

\* Not an unbiased estimate: vitts 0.1 was tuned on dev, and the vitts 0.2 rules were written after looking at v1 errors.
</details>

**Method.** Each vitts version is measured on a held-out set written *before* that version, and code is never tuned on it; the git history shows the order. References are hand-written, a sentence may have several correct readings, and regional variants (*ngàn/nghìn, lẻ/linh, tỉ/tỷ…*) are merged before scoring ([`metrics.py`](../src/vitts/bench/metrics.py)). **Limitation:** the sets are small and written by one person. Per-sentence outputs: [`results/normalization_heldout_v2_errors.md`](../results/normalization_heldout_v2_errors.md).

## Loanword transliteration

`vitts.translit` is a 5.6M-parameter character-level Transformer that reads a word (plus its [CMUdict](https://github.com/cmusphinx/cmudict) phonemes when available) and writes its Vietnamese reading, e.g. "container" → "công tê nơ". It is trained on 17.7k hand-written pairs from [vietnormalizer](https://github.com/nghimestudio/vietnormalizer) (MIT), split train/dev/test **by word stem**, and its configuration was chosen on dev only.

### Blind human review

150 random test words were reviewed by one native speaker. The reviewer saw every candidate reading (dictionary, this model, gpt-4o-mini, Qwen, rules, plus 3 GPT alternatives), shuffled and without sources, and marked the acceptable ones ([review page](https://yoonjae26.github.io/vietnamese-tts/review/), [source](review/), [data](../data/translit/review/)).

| System | Accepted (149 words) | 95% CI |
|---|---:|---:|
| gpt-4o-mini, few-shot (OpenAI API) | **30.9%** | 23.5–38.3% |
| gpt-4o-mini, zero-shot | 30.2% | |
| Training dictionary itself | 27.5% | 20.8–34.9% |
| **vitts translit (5.6M params, 0.1 GB VRAM)** | **24.8%** | 18.1–32.2% |
| Qwen2.5-7B-Instruct, few-shot (7.6B params) | 14.8% | 9.4–20.8% |
| vietnormalizer rules | 4.0% | |

- **On par with gpt-4o-mini:** GPT is 6 points ahead, but the 95% CI of the paired difference is −4 to +16 points.
- **Better than Qwen2.5-7B** with statistical significance (+10 points, 95% CI +0.7 to +19.5). Qwen keeps English, inserts Chinese characters or invents letters ([raw outputs](../results/translit_llm_raw_examples.txt)).
- **The training dictionary is accepted only 27.5% of the time**, and the model lands at the same level.
- **Limitations:** one reviewer; the reviewer usually accepted only their single preferred reading (138 of 150 words); each word had up to 5 GPT-style candidates versus 1 from every other system.

<details>
<summary>Automatic scoring against the dictionary (1,676 unseen words)</summary>

| System | Exact match ↑ | Syllable error ↓ |
|---|---:|---:|
| soe-vinorm | 0.5% | 110.5% |
| vietnormalizer rules (no dictionary lookup) | 7.8% | 73.1% |
| vitts translit v1 (letters only) | 47.1% | 37.2% |
| **vitts translit (letters + CMUdict phonemes)** | **55.1%** | **30.0%** |
| Qwen2.5-7B-Instruct zero-shot / few-shot | 3.2% / 4.2% | 95.3% / 95.9% |
| gpt-4o-mini zero-shot / few-shot | 15.9% / 19.6% | 75.5% / 66.4% |

This scoring favors the model, which learned the dictionary's spelling conventions ("s" → "x", "f" → "ph"), while GPT writes "sam sung" or "nét flích" and is marked wrong. That is why the human review is the headline. Evaluating gpt-4o-mini on 1,676 words cost about 67k tokens ([script](../training/translit/api_baseline.py)).

| Configuration (tuned on dev) | Dev |
|---|---:|
| d256, 3 layers, dropout 0.1 | 47.3% |
| d256, 3 layers, dropout 0.2 | 51.7% |
| d384, 4 layers, dropout 0.2 | 52.3% |
| **d256, 3 layers, dropout 0.2, + phonemes** (selected) | **53.1%** |
| d384, 4 layers, dropout 0.2, + phonemes | 53.1% |
</details>

### Negative result: relabeling with GPT

All 16k train/dev words were relabeled with gpt-4o-mini (about 390k tokens, [script](../training/translit/relabel_gpt.py)). The model was retrained with the same configuration and scored once on the 149 reviewed words:

| Training labels | Accepted by reviewer | vs. gpt-4o-mini (95% CI) |
|---|---:|---:|
| **Dictionary (default)** | **24.8%** | −6.0% (−16.1% to +4.0%) |
| Dictionary + GPT | 24.2% | −6.7% (−16.1% to +2.7%) |
| GPT only | 12.8% | −18.1% (−24.8% to −11.4%) |

GPT labels **halved** accuracy. 11% of them still contain Latin fragments ("blai th"), and GPT reads each word from its own knowledge rather than a consistent rule, so the small model learns the noise without the knowledge. Better results need consistent human labels and more reviewers.

## Reproduce

```bash
pip install -e ".[bench,translit]"

# Text normalization
python benchmark/normalization/build_testset.py
python benchmark/normalization/run.py --split heldout_v2

# TTS: one conda env per model (model sources are cloned into ~/vitts-engines)
bash benchmark/tts/envs/coqui.sh      # also f5.sh, vieneu.sh, viettts.sh, indextts.sh
bash benchmark/tts/run_all.sh         # synthesize with every model, then score

# Transliteration model
python training/translit/prepare_data.py
bash training/translit/sweep.sh
CUDA_VISIBLE_DEVICES=0 python training/translit/evaluate.py
```

GPU scripts refuse to run unless `CUDA_VISIBLE_DEVICES=0`; change `ALLOWED_GPU` in [`benchmark/tts/synthesize.py`](../benchmark/tts/synthesize.py) for your machine.

## Roadmap

- [ ] Human MOS; several reference voices (male, female, studio, phone)
- [ ] Time to first audio when streaming; CPU RTF for every model
- [ ] API: streaming audio, choose the reference voice with `voice`
- [ ] Transliteration: labels from several reviewers; batched decoding or ONNX; non-English names
- [ ] Normalization: held-out v3 written by several people
