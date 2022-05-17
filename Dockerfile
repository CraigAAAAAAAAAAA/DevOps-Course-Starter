#Stage 1 - base
FROM python:3.10-slim-bullseye as build
WORKDIR /app
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=$PATH:/root/.poetry/bin
COPY poetry.lock poetry.toml pyproject.toml /app/
RUN poetry install --no-dev
COPY todo_app ./todo_app

#Stage 2 - development
FROM build as development
RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0
EXPOSE 5000

#Stage 3 - production
FROM build as production
ENTRYPOINT poetry run gunicorn --bind=0.0.0.0 "todo_app.app:create_app()"
EXPOSE 8000

#Stage 4 - testing
FROM build as test
RUN pip install pytest
RUN poetry run pytest
