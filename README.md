[![CircleCI](https://circleci.com/gh/t04st3r/django-celery.svg?style=shield)](https://app.circleci.com/pipelines/github/t04st3r/django-celery) [![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


# django-celery
This is a sample project used as a base for django related projects.

## Install
To run django locally you need python version to `3.11.3` and pipenv, you can use [pyenv](https://github.com/pyenv/pyenv) to set your desired python version.

### Run containers
Django needs postgres and redis container to be
up and running, to do so clone the project, enter in the project folder and hit:
```bash
docker compose up postgres redis maildev celery
```

### Install django deps and run django server
inside the project folder make sure you use python 3.11.3
```bash
python --version
```
you should see
```bash
Python 3.11.3
```
install requirements (listed inside `Pipfile`) by
```bash
pipenv install
```
To run tests you will need also dev dependencies
```bash
pipenv install --dev
```
Create a `.env` file using the `.env.example` file and changing the url to be `localhost` in the following env variables:
```env
POSTGRES_HOST
REDIS_URL
EMAIL_HOST
CELERY_BROKER_URL
CELERY_RESULT_BACKEND
```
Your `.env` file should be something like this
```env
#django
ENV=ci
DJANGO_DEBUG=True
SECRET_KEY='supersecretkey'
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_HOST_USER=dev
EMAIL_HOST_PASSWORD=dev

#db
POSTGRES_USER=postgres
POSTGRES_DB=app_db
POSTGRES_HOST=localhost
POSTGRES_PASSWORD=password
POSTGRES_PORT=5432

#redis
REDIS_URL=redis://localhost:6379/0

#celery
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379

```

Once done enter inside your pipenv virtual environment by
```bash
pipenv shell
```
Run migrations with
```bash 
python manage.py migrate
```
Or (if you have `make` installed) by
```bash
make migrate
```
Everything is done! You can now start the server with
```bash
python manage.py runserver
```
Or
```bash
make run-dev
```
## How does it works
This apps gather data from [Public Holiday API](https://date.nager.at/Api) via a django command, you can populate PublicHoliday models with
```bash
python manage.py populate_models
```
Or
```bash
make populate-models
```
For each command run a random country is selected and all the public holidays for that country would be fetched and stored in the db.

Anytime a `PublicHoliday` model object is created/updated
a signal is dispatched that, in turn, will schedule a celery task that will basically send an email with the JSON representation of the object. The email are not really sent but will be collected by the `maildev` container.

You can test this flow by trying to change a property, or create a new model via the `django admin`.
In order to login in the `django admin` you need to create a superuser. It can be done by hitting:
```bash
python manage.py createsuperuser
```
To test the correct `celery` task execution you can connect to the `maildev` web interface at the url:
```
http://localhost:1080
```
You should see the mail being sent from the `celery` task (see also `public_holiday.tasks.py` and `public_holiday.signals.py`)


## Testing
Testing requirements can be installed by
```bash
pipenv install --dev
```
To run the ruff linter on your codebase hit
```bash
make lint
```
pre-commit (that in turn will run ruff check) can be installed as well with
```bash
pre-commit install
``` 
You can run django tests by simply run
```bash
pytest
```
To simulate the [testing pipeline](https://app.circleci.com/pipelines/github/t04st3r/django-celery) in CircleCI just run
```bash
docker compose run django ci
```