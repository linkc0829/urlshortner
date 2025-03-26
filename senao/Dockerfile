FROM python:3.13-alpine

RUN apk update && apk add python3-dev gcc libc-dev bash

WORKDIR /app/

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/