FROM ubuntu:18.04

LABEL "app.name"="MOS Backend"

# Python
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

# Python dependencies
ADD ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

# Optdev-backend
ADD . /mos-backend

# CMD
WORKDIR /mos-backend
ENTRYPOINT ["./manage.py", "run_mos_backend"]