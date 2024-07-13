FROM python:3.11-slim

LABEL authors="Dmitry"

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
COPY db app/db/
COPY gigaChat app/gigaChat/
COPY bot app/bot/
COPY parsers app/parsers/
COPY requirements.txt .

RUN python3 -m pip install --upgrade pip && \
    pip3 install --use-pep517 --no-cache-dir -r requirements.txt

COPY . .
RUN cd /app/bot
CMD ["python3", "__init__.py"]
EXPOSE 8080
