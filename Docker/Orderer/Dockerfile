FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \

        build-essential \

        curl \

        git \

        libssl-dev \

        libffi-dev \

        python3-dev \

    && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv

WORKDIR /code

COPY Pipfile* ./

RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

EXPOSE 5001

CMD ["python", "bcb_server/orderer.py"]

