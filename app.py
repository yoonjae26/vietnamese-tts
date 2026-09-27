"""Demo Gradio. Chạy: `python app.py` (dùng được làm Hugging Face Space)."""

import os

import gradio as gr

from vitts import normalize_text
from vitts.synthesizer import DEFAULT_MODEL, VietnameseTTS

tts = VietnameseTTS(
    model_name=os.getenv("VITTS_MODEL_NAME", DEFAULT_MODEL),
    model_path=os.getenv("VITTS_MODEL_PATH"),
    config_path=os.getenv("VITTS_CONFIG_PATH"),
)

EXAMPLES = [
    ["Xin chào! Hôm nay là ngày 2/9/2024, nhiệt độ ở TP.HCM khoảng 33°C.", 1.0],
    ["Giá vàng tăng 1.250.000đ/lượng, tức khoảng 1,5% so với tuần trước.", 1.0],
    ["Đội tuyển U23 VN thắng 3-1 lúc 19h30 tối thứ 4.", 1.1],
]


def run(text: str, speed: float):
    audio = tts.synthesize(text, speed=speed)
    return (audio.sample_rate, audio.samples), normalize_text(text)


demo = gr.Interface(
    fn=run,
    inputs=[
        gr.Textbox(label="Văn bản", lines=4, placeholder="Nhập văn bản tiếng Việt..."),
        gr.Slider(0.5, 2.0, value=1.0, step=0.05, label="Tốc độ"),
    ],
    outputs=[gr.Audio(label="Giọng đọc"), gr.Textbox(label="Văn bản sau chuẩn hóa")],
    examples=EXAMPLES,
    title="🇻🇳 Vietnamese TTS",
    description="Chuyển văn bản tiếng Việt thành giọng nói. Tự động đọc số, ngày giờ, tiền tệ, đơn vị và chữ viết tắt.",
)

if __name__ == "__main__":
    demo.launch()
