"""Huấn luyện VITS tiếng Việt (1 người nói) bằng coqui-tts.

Chuẩn bị dữ liệu dạng:
    data/my_dataset/
        metadata.csv      # mỗi dòng: <id>|<văn bản>
        wavs/<id>.wav     # mono, 22050 Hz

Chạy:
    python recipes/vits/train_vits.py --data data/my_dataset
    tensorboard --logdir runs/
"""

import argparse
import os

from trainer import Trainer, TrainerArgs
from TTS.tts.configs.shared_configs import BaseDatasetConfig, CharactersConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsAudioConfig
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

from vitts.datasets import FORMATTERS
from vitts.text import CHARACTERS, PUNCTUATIONS, normalize_text

parser = argparse.ArgumentParser()
parser.add_argument("--data", required=True, help="thư mục dataset")
parser.add_argument("--formatter", default="vi_ljspeech", choices=list(FORMATTERS))
parser.add_argument("--meta-file", default="metadata.csv")
parser.add_argument("--output", default="runs")
parser.add_argument("--batch-size", type=int, default=32)
parser.add_argument("--epochs", type=int, default=1000)
parser.add_argument("--restore-path", default=None, help="checkpoint để fine-tune tiếp")
args = parser.parse_args()

dataset_config = BaseDatasetConfig(formatter=args.formatter, meta_file_train=args.meta_file, path=args.data)
audio_config = VitsAudioConfig(
    sample_rate=22050, win_length=1024, hop_length=256, num_mels=80, mel_fmin=0, mel_fmax=None
)

config = VitsConfig(
    audio=audio_config,
    run_name="vits_vietnamese",
    batch_size=args.batch_size,
    eval_batch_size=16,
    batch_group_size=5,
    num_loader_workers=4,
    num_eval_loader_workers=2,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=args.epochs,
    # Văn bản đã được vitts chuẩn hóa trong formatter -> chỉ cần hạ chữ thường + gộp khoảng trắng
    text_cleaner="basic_cleaners",
    use_phonemes=False,
    characters=CharactersConfig(
        characters_class="TTS.tts.models.vits.VitsCharacters",
        pad="_",
        eos="&",
        bos="*",
        blank=None,
        characters=CHARACTERS,
        punctuations=PUNCTUATIONS,
        phonemes=None,
    ),
    compute_input_seq_cache=True,
    print_step=25,
    print_eval=True,
    mixed_precision=True,
    output_path=args.output,
    datasets=[dataset_config],
    cudnn_benchmark=False,
    test_sentences=[
        normalize_text("Xin chào, tôi là trợ lý giọng nói tiếng Việt."),
        normalize_text("Hôm nay ngày 2/9/2024, trời Hà Nội khoảng 30°C."),
        normalize_text("Giá bán là 1.250.000đ, giảm 15% so với tháng trước."),
    ],
)

ap = AudioProcessor.init_from_config(config)
tokenizer, config = TTSTokenizer.init_from_config(config)

train_samples, eval_samples = load_tts_samples(
    dataset_config,
    eval_split=True,
    eval_split_max_size=config.eval_split_max_size,
    eval_split_size=config.eval_split_size,
    formatter=FORMATTERS[args.formatter],
)

model = Vits(config, ap, tokenizer, speaker_manager=None)

trainer = Trainer(
    TrainerArgs(restore_path=args.restore_path),
    config,
    os.path.abspath(args.output),
    model=model,
    train_samples=train_samples,
    eval_samples=eval_samples,
)
trainer.fit()
