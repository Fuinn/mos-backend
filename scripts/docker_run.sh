#!/bin/bash
sudo docker run -it \
                --rm \
                --network=host \
                -v mos-backend-media:/mos-backend/service/media \
                --env-file=.env \
                --name=mos-backend \
                tomastinoco/mos-backend