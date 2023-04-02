FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev \

    && pip install --no-cache-dir -r requirements.txt \

    && apk del .build-deps

COPY . /app

CMD ["python", "app.py"]

