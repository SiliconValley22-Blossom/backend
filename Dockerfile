FROM python:3.9.13-slim

WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /backend/
