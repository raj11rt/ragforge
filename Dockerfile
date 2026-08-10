FROM python:3.12-slim

WORKDIR /app

# Install supervisor (process manager to run API + dashboard together)
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv
RUN uv sync --frozen

COPY . .

# Create runtime directories
RUN mkdir -p /data/chroma_db app/storage/uploads app/storage/extracted

# HF Spaces requires port 7860 (Streamlit dashboard)
# FastAPI runs internally on port 8000
EXPOSE 7860

CMD ["/usr/bin/supervisord", "-c", "/app/supervisord.conf"]