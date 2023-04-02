FROM python:3.9-slim-buster

COPY . /code

WORKDIR /code

RUN apt-get update && \

    apt-get install -y build-essential && \

    pip install poetry && \

    poetry install --no-dev

ENTRYPOINT ["python", "bcb_server/peer.py", "--ca", "0.0.0.0", "--orderer", "0.0.0.0"]

