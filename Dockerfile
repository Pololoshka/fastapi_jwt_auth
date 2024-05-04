FROM python:3.12

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=true

# Install poetry
RUN pip install poetry
ENV PATH="$POETRY_HOME/bin:$HOME/.local/bin:$PATH"

WORKDIR /app

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry install --only main

COPY ./src/ ./src/
COPY ./preload_data/ ./preload_data/

COPY ./alembic.ini .
