FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry install --with dev

RUN apt-get update
RUN apt-get install postgresql-client -y

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
