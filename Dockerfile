FROM python:3.11-slim

LABEL authors="Dmitry"
LABEL org.opencontainers.image.title="My Python Bot"
LABEL org.opencontainers.image.description="A Python-based bot application"
LABEL org.opencontainers.image.source="https://github.com/your-username/your-repo"

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --use-pep517 --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python3", "bot/front.py"]
EXPOSE 8080
