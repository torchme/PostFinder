FROM python:3.11.6

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install

RUN chmod +x /app/docker/bot.sh
