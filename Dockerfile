#Stage 1 - base
FROM python:3.10-slim-bullseye as build
WORKDIR /app
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=$PATH:/root/.poetry/bin
COPY poetry.lock poetry.toml pyproject.toml /app/
RUN poetry config virtualenvs.create false --local && poetry install
COPY todo_app ./todo_app

#Stage 2 - development
FROM build as development
RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0
EXPOSE 5000

#Stage 3 - testing
FROM development as test
ENV GECKODRIVER_VER v0.31.0
 
# Install the long-term support version of Firefox (and curl if you don't have it already)
RUN apt-get update && apt-get install -y firefox-esr curl
  
# Download geckodriver and put it in the usr/bin folder
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz

ENTRYPOINT ["poetry", "run", "pytest"]

#Stage 4 - watchdogtest
FROM test as watchdogtest
ENTRYPOINT poetry run watchmedo shell-command --patterns="*.py;*.html" --recursive --command="poetry run pytest"

#Stage 5 - production - this stage needs to be last otherwise the CD pipeline through Heroku will not work
FROM build as production
ENV PORT=8000
COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh
EXPOSE 8000