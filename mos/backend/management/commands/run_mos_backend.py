import os

from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line    

class Command(BaseCommand):

    def handle(self, *args, **options):

        host = os.getenv('MOS_BACKEND_HOST', 'localhost')
        port = os.getenv('MOS_BACKEND_PORT', 8000)
        location = '%s:%s' %(host, port)
        execute_from_command_line(['', 'migrate', '--noinput'])
        execute_from_command_line(['', 'collectstatic', '--noinput'])
        execute_from_command_line(['', 'runserver', location, '--insecure'])