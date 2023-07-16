FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install postgresql-client python3-dev gcc -y

RUN pip install poetry
RUN poetry install --with dev

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
