# Start Dockerized Django

## Quick start
```shell
$ docker-compose build
$ docker-compose up -d
$ docker-compose exec app python manage.py makemigrations # run this only if you change database
$ docker-compose exec app python manage.py migrate
$ docker-compose exec app python manage.py createsuperuser
$ docker-compose exec app python manage.py collectstatic
```

## Installation

First, [install Docker](https://docs.docker.com/installation/) and [Docker Compose](https://docs.docker.com/compose/install/). If you're new to Docker, you might also want to check out the [Hello, world! tutorial](https://docs.docker.com/userguide/dockerizing/).

Next, clone this repo:
```shell
$ git clone https://github.com/KhasanovR/startDockerizedDjango.git
$ cd startDockerizedDjango
```

## Configuration

First, [install Docker](https://docs.docker.com/installation/) and [Docker Compose](https://docs.docker.com/compose/install/). If you're new to Docker, you might also want to check out the [Hello, world! tutorial](https://docs.docker.com/userguide/dockerizing/).

Next, clone this repo:
```dotenv
DOCKER_REPOSITORY={{your INPUT}}
DOCKER_REPOSITORY={{your INPUT}}
DOCKER_NGINX_VERSION=1.0
DOCKER_APP_VERSION=0.1
POSTGRES_USER={{your INPUT}}
POSTGRES_DB={{your INPUT}}
POSTGRES_PASSWORD={{your INPUT}}
CELERY_WORKER_LOGLEVEL=DEBUG
CELERY_BEAT_LOGLEVEL=DEBUG
PRODUCTION_HOST={{your INPUT}}
DEBUG=True(optional){{your INPUT}}
SECRET_KEY={{your INPUT}}
ALLOWED_HOSTS={{your INPUT}},localhost,127.0.0.1,0.0.0.0
MEDIA_URL=/media/
DATABASE_URL={{your INPUT}}
CELERY_BROKER_URL=redis://redis:6379/1
GUNICORN_WORKERS=1
```
