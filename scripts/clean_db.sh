#!/bin/bash
echo cleaning mos-backend database ...
sudo -u postgres dropuser mos
sudo -u postgres dropdb mos
rm -rf ./mos/media