#!/bin/bash
echo cleaning mos-backend migrations ...
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

