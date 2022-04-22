FROM python:3

LABEL "app.name"="MOS Backend"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Python dependencies
ADD ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# MOS backend files
ADD . /mos-backend

# Entrypoint
WORKDIR /mos-backend
ENTRYPOINT ["./manage.py", "run_mos_backend"]