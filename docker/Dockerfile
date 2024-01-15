FROM python:3.10.1

WORKDIR /app

COPY . /app

RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "bash", "run_bot.sh"]
