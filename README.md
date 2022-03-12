# mos-backend

MOS backend server.

## Pre-requisites

### Services

* postgresql
* redis
* rabbitmq

### Environment variables

* MOS_BACKEND_DEBUG
* MOS_BACKEND_HOST
* MOS_BACKEND_PORT
* MOS_BACKEND_SECRET
* MOS_FRONTEND_HOST
* MOS_FRONTEND_PORT
* MOS_DATABASE_NAME
* MOS_DATABASE_USR
* MOS_DATABASE_PWD
* MOS_DATABASE_HOST
* MOS_DATABASE_PORT
* MOS_REDIS_DB
* MOS_REDIS_PORT
* MOS_REDIS_HOST
* MOS_RABBIT_PORT
* MOS_RABBIT_USR
* MOS_RABBIT_PWD
* MOS_RABBIT_HOST

### Python dependencies

Install Python dependencies with

``sudo pip3 install -r requirements.txt``

## Local Deployment

Run the MOS backend using 

``./manage.py run_mos_backend``

Create an admin user with

``./manage.py createsuperuser``

The following endpoints are then available and accessible:

* REST api: ``MOS_BACKEND_HOST:MOS_BACKEND_PORT/api``
* admin site: ``MOS_BACKEND_HOST:MOS_BACKEND_PORT/admin``

## Dockerized Deployment

* ``./scripts/docker_build.sh``: Build MOS Backend image.
* ``./scripts/docker_run.sh``: Runs MOS Backend container.
* ``./scripts/docker_createsuperuser.sh``: Creates super user (containers needs to be running).
