#!/bin/bash
echo creating mos-backend database ...
sudo -u postgres createuser mos
sudo -u postgres createdb -O mos mos
sudo -u postgres psql -c "alter user mos with encrypted password 'mos'"
sudo -u postgres psql -c "grant all privileges on database mos to mos"