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

* MOS_BACKEND_DEBUG:
* MOS_BACKEND_HOST:
* MOS_BACKEND_PORT:
* MOS_BACKEND_SECRET:
* MOS_ADMIN_USR:
* MOS_ADMIN_PWD:
* MOS_ADMIN_EMAIL:
* MOS_EMAIL_USR:
* MOS_EMAIL_PWD:
* MOS_FRONTEND_HOST:
* MOS_FRONTEND_PORT:
* MOS_DATABASE_NAME:
* MOS_DATABASE_USR:
* MOS_DATABASE_PWD:
* MOS_DATABASE_HOST:
* MOS_DATABASE_PORT:
* MOS_REDIS_DB:
* MOS_REDIS_PORT:
* MOS_REDIS_HOST:
* MOS_RABBIT_PORT:
* MOS_RABBIT_USR:
* MOS_RABBIT_PWD:
* MOS_RABBIT_HOST:

## Local Deployment

Install Python dependencies with

``sudo pip install -r requirements.txt``

Run the MOS backend using 

``./manage.py run_mos_backend``

The following endpoints are then available:

* REST api: ``MOS_BACKEND_HOST:MOS_BACKEND_PORT/api``
* admin site: ``MOS_BACKEND_HOST:MOS_BACKEND_PORT/admin``

## Dockerized Deployment

The following scripts are available for building the image, running the container, connecting to the container, and for pushing the image to Docker Hub:

* ``./scripts/docker_build.sh``
* ``./scripts/docker_run.sh``
* ``./scripts/docker_connect.sh``
* ``./scripts/docker_push.sh``

## Citation

If MOS is useful for research purposes, [the MOS overview paper](https://fuinn.ie/mos.pdf) may be cited.
