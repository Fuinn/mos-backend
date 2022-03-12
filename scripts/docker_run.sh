#!/bin/bash
sudo docker run -it --rm --network=host -v mos-backend-media:/mos-backend/service/media --name mos-backend mos-backend