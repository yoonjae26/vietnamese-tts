FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends espeak-ng libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir ".[server]"

# Tải model khi build để container khởi động nhanh
RUN python -c "from vitts.synthesizer import VietnameseTTS; VietnameseTTS()"

EXPOSE 8000
CMD ["vitts-server", "--local", "--host", "0.0.0.0", "--port", "8000"]
