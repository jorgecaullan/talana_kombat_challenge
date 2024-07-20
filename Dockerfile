FROM python:3.12-slim

WORKDIR /talana_kombat

COPY src/requirements.txt .
RUN pip install -r requirements.txt

COPY src .
