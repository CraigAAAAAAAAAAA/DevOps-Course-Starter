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

## Create Trello account

To use the app you'll need to create a Trello account at www.trello.com and from there set up a board, lists and cards. Once this is done populate the .env file with the following:
•	TRELLO_API_KEY
•	TRELLO_TOKEN
•	TRELLO_BOARD_ID

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