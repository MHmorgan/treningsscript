# syntax=docker/dockerfile:1

# Docker file with gunicorn?
# https://github.com/tiangolo/uvicorn-gunicorn-docker

FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "8000"]
