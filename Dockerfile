FROM python:3.9.13-slim

WORKDIR /backend
COPY requirements.txt /backend/

ADD . /tmp/latest

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY ./myapp/ /backend/myapp/
ENV FLASK_APP myapp
ENV PROMETHEUS_MULTIPROC_DIR /tmp
ENV prometheus_multiproc_dir /tmp

COPY . /backend/
