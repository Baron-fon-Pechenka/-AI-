FROM ubuntu:latest
LABEL authors="Dmitry"

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y python3
CMD ["python3", "bot/front.py"]
EXPOSE 8080
