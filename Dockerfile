FROM python:3.13
LABEL maintainer="galytskiyihor@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install --upgrade pip

COPY . .
