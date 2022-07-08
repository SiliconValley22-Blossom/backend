# pull official base image
FROM python:3.9.13-slim

RUN pip install --upgrade pip
RUN pip3 install flask

WORKDIR /backend
# COPY requirements.txt /backend/

# RUN apk add postgresql-dev libressl-dev libffi-dev gcc musl-dev gcc python3-dev musl-dev zlib-dev jpeg-dev #--(5.2)


# RUN pip install -r requirements.txt

COPY . /backend/
