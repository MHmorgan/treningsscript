# syntax=docker/dockerfile:1

# Docker file with gunicorn?
# https://github.com/tiangolo/uvicorn-gunicorn-docker

FROM python:3.11-alpine

ENV DATABASE="/data/trapp.sqlite"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

#CMD ["python3", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "8000"]
CMD ["python3", "-m", "gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "app:create_app()"]
