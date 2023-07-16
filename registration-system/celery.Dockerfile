FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry install --with dev

CMD [ "poetry", "run", "task", "celery", "--logfile=logs/celery.log" ]
