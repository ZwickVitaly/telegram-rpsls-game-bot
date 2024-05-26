FROM python:3.10-alpine
LABEL authors="zwickvitaly"

WORKDIR /bot

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY bot/ .

ENTRYPOINT python3 main.py


