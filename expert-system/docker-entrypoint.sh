#!/bin/bash

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - executing command"

# Download the nltk packages
poetry run python -c "import nltk;nltk.download('averaged_perceptron_tagger_ru');nltk.download('stopwords');nltk.download('wordnet');nltk.download('punkt');"

poetry run task makemigrations
poetry run task migrate
poetry run task createsuperuser --noinput
poetry run task start 0:8000

exec "$@"
