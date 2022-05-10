#Stage 1 - Base
FROM python:3.10-slim-bullseye as build
WORKDIR /app
RUN apt-get update
RUN apt-get install -y curl
COPY . /app
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=$PATH:/root/.poetry/bin
RUN poetry install

#Stage 2 - Development
FROM build as development
COPY --from=build /app /app
WORKDIR /app
ENTRYPOINT poetry run flask --bind=0.0.0.0 todo_app.app
EXPOSE 5000


#Stage 3 - Production
FROM build as production
COPY --from=build /app /app
WORKDIR /app
ENTRYPOINT poetry run gunicorn --bind=0.0.0.0 "todo_app.app:create_app()"
EXPOSE 8000



