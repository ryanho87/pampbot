# syntax=docker/dockerfile:1

# install python
FROM python:3.9-slim-buster
USER root

ENV TOKEN = ""

WORKDIR /pampbot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pampbot.py .

CMD ["python3", "-u","./pampbot.py"]