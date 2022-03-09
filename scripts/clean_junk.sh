#!/bin/bash
echo cleaning mos-backend junk ...
find . -name \*~ -delete
find . -name "*.pyc" -type f -delete
find . -name __pycache__ -delete

