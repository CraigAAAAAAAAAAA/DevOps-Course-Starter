#Stage 1 - base
FROM python:3.10-slim-bullseye as build
WORKDIR /app
RUN apt-get update && apt-get install -y curl
COPY . /app
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=$PATH:/root/.poetry/bin
RUN poetry install

#Stage 2 - development
FROM build as development
WORKDIR /app
ENTRYPOINT poetry run flask --bind=0.0.0.0 todo_app.app
EXPOSE 5000


#Stage 3 - production
FROM build as production
WORKDIR /app
ENTRYPOINT poetry run gunicorn --bind=0.0.0.0 "todo_app.app:create_app()"
EXPOSE 8000