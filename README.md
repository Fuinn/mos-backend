# mos-backend

MOS backend server.

## Pre-requisites

### Services

* postgresql
* redis
* rabbitmq

### Environment variables

The following environment variables can be specified.
They can be provided via a .env file.

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

## Local Deployment

Install Python dependencies with

``sudo pip install -r requirements.txt``

Run the MOS backend using 

``./manage.py run_mos_backend``

Create an admin user with

``./manage.py createsuperuser``

The following endpoints are then available and accessible:

* REST api: ``MOS_BACKEND_HOST:MOS_BACKEND_PORT/api``
* admin site: ``MOS_BACKEND_HOST:MOS_BACKEND_PORT/admin``

## Dockerized Deployment

* ``./scripts/docker_build.sh``: Builds MOS Backend image.
* ``./scripts/docker_run.sh``: Runs MOS Backend container.
* ``./scripts/docker_createsuperuser.sh``: Creates admin user (container needs to be running).

The following endpoints are then available and accessible:

* REST api: ``MOS_BACKEND_HOST:MOS_BACKEND_PORT/api``
* admin site: ``MOS_BACKEND_HOST:MOS_BACKEND_PORT/admin``

## Citation

If MOS is useful for research purposes, [the MOS overview paper](https://fuinn.ie/mos.pdf) may be cited.
