# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

This project contains 2 units tests, the first test checks that a new task called 'answer emails' appears in the correct "to do" list not any of the other lists. The second unit test tests that the task "go home" has gone into the "done items" list. 

There is also an integration test which use mocked data from .env.test to ensure there is a response from Trello and that a new card is added to a list. 

Additionally test_e2e.py tests that a board can be set up and deleted. 

To execute the tests run: poetry run pytest on the command line.

## SSH and running from VM/Ansible

Ansible controller IP: 13.40.253.177
Managed node IP: 3.9.109.19

Passwords are already set up to access them

run ssh ec2-user@13.40.253.177 or ssh ec2-user@3.9.109.19 respectively to access them.

To run the Ansible playbook use the following command from the control node:
$ ansible-playbook exercise-4-playbook.yml -i my-ansible-inventory --vault-password-file vault_password.txt

use the folowing address to check the to-do app is working:
http://3.9.109.19:5000/

Note the above link will not work once the VM's are torn down.

For more information on using ansible modules - see https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html

## Docker

Ensure you have Docker Desktop installed. Visit: https://www.docker.com/products/docker-desktop/
For Windows: https://docs.docker.com/desktop/windows/install/

Sign up up for a free Docker account: https://hub.docker.com/signup

Docker Desktop will need to be running for the images and containers to work.

Install the Docker extension in VS Code

A multistaged dockerfile has been set up which includes a base build, a dev build and a production build. The dev build uses Flask to run whilst Development is using Gunicorn.

The dev image is using port 5000 
The prod image is using port 8000

## Building containers - commands:

To build the dev container - input the following command in the terminal:

docker build --target development --tag todo_app:dev .

To build the prod container - input the following command in the terminal:

docker build --target production --tag todo_app:prod .

## Running Containers:

To run the dev container with a bind mount to allow live updates in the todo application use the following command:

docker run --env-file .env -p 5000:5000 --mount type=bind,source=$(pwd)/todo_app,target=/app/todo_app todo_app:dev

To run the prod container:

docker run --env-file .env -p 8000:8000 -it  todo_app:prod
This container doesn't require a bind mount displaying live app changes updates since this should be done in the dev environment. 

## To view the app:
Run the containers then in a browser type:

localhost:5000 - Dev
localhost:8000 - Prod

To view the Docker documentation visit - https://docs.docker.com/get-started/overview/
To change the base image tag e.g. python:3.10-slim-bullseye visit: https://hub.docker.com/_/python
note - this is a python app so you'll need to use one specific to python. Remember to rebuild the image after any changes are made to the dockerfile. 

To remove unwanted container use the following command in the terminal - docker container prune
This removes all of them, to remove them individually in VS Code right click on the container to be removed and select remove. 
Make sure the container has been stopped before its removed. 

## Docker Compose

To run the containers using the docker-compose.yml file type 'docker compose up' in the terminal. This will run both the dev and prod environments without needing to write long commands running them individually. To take them down again press ctrl c. 

Refresh the dev environment on localhost:5000 to see any changes made to the application. 

## Testing in Docker

To run the test container use the following commands in the terminal:

Build:
docker build --target test --tag todo_app:test .  

Run integration tests:
docker run --env-file .env.test todo_app:test todo_app/tests/test_app.py

Run unit tests:
docker run --env-file .env.test todo_app:test todo_app/tests/test_unit.py

Run E2E tests:
docker run -e MONGO_CONNECTION_STRING='${{secrets.MONGO_CONNECTION_STRING}}' -e MONGO_DATABASE_NAME='${{secrets.MONGO_DATABASE_NAME}}' -e SECRET_KEY=anything todo_app:test todo_app/tests/test_e2e.py

To run tests whenever a change is made utilising Watchdog's watchmedo feature run the following in the command line:

poetry run watchmedo shell-command --patterns="*.py;*.html" --recursive --command="poetry run pytest"

This command looks for any changes in files ending .py or .html. 

To buid and run a container that runs tests when changes are made, use:

docker build --target watchdogtest --tag todo_app:watchdogtest .

docker run --env-file .env.test --mount type=bind,source=$(pwd)/todo_app,target=/app/todo_app todo_app:watchdogtest

Or to run it as part of the Docker Compose .yml file use Docker Compose Up as before.

## Continuous Integration
Tests have been configured to set up and run docker containers everytime there is a push or pull on the repo, as well at 23:00 UTC without any changes being made. 

## Security Scan
As part of the CI tests, Synk is used to check for any vulnerabilities in the code. 

## Continuous Deployment
After tests are complete, the app is set up to continually deploy when there is a push to the main branch. It pushes a production image to Docker Hub and to Heroku

## Deployment
The to-do app is deployed via Azure at https://my-stuff-todo.azurewebsites.net

## MongoDB
The code has been updated to use MongoDB to hold tasks added to the app, change the status to in progress and then delete document from the collection when its been completed. 

Testing has been updated to reflect the move away from Trello and now tests that the DB works as expected and that the app can still be set up and taken down. 

## OAuth
Authorisation is now required via Github to access the To-Do app. New code added to redirect users to Github to log in, authenticated users will be able to view the To-Do app but only users with 'Writing' access will be able to add tasks and modify existing tasks. 
The login function has been disabled on tests to allow these to run. 

## Terraform
The app's architecture is now configured using terraform. It provisions the mongo database and utilities blob storage. The CI/CD pipeline has been updated to include terraform with no sensitive variables appearing in the logs. 

Secrets should be added to the terraform.tfvars file, be sure to add this file to .gitignore file.  A description of the variables and secrets should added to the variables.tf file, setting to 'true' any sensitive variables.

To set up terraform locally once the files are configured type in the following commands in the CLI:
- terraform init 
- terraform plan - this will allow you to see what terraform is setting up
- terraform apply - this is to apply the changes you want to make

Prevent Destroy is currently set to true in the main.tf file, to remove the current resources and start again this will either need to be set to false or commented out.

## Logging
Logging has been set up to store logs at info level and above. Logs are stored at loggly.com and stores the following:
- Item ID when the user clicks on start and complete 
- The logs the tile of the task, this could potential store private information but for the purposes of this exercise   deemed it was ok. 
- Error logs set up to record if tasks do not behave as expected e.g. does not change status to started when the corresponding button is clicked.
-Warning logs set to record the user ID when an authorised user logs into the app, when a new user visits the app or when a user with no write access tries to edit the tasks


