FROM python:3.10-bullseye
WORKDIR /app
RUN apt-get update
RUN apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN poetry /bin/poetry
COPY . /app/
ENTRYPOINT [ ""./todo_app"" ]
CMD [ "run flask run"]
EXPOSE 8080/tcp