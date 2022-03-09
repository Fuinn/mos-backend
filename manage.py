#!/usr/bin/env python3
import os
import sys

from django.core.management import execute_from_command_line

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
    execute_from_command_line(sys.argv)
