import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, UserManager

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        if User.objects.filter(is_superuser=True).count() == 0:
            usr = os.getenv('MOS_ADMIN_USR', '')
            pwd = os.getenv('MOS_ADMIN_PWD', '')
            email = os.getenv('MOS_ADMIN_EMAIL', '')
            if usr and pwd and email:
                print('Creating admin user %s' % usr)
                admin = User.objects.create_superuser(email=email, username=usr, password=pwd)
                admin.is_active = True
                admin.is_superuser = True
                admin.save()
            else:
                print('Unable to create admin user (missing data)')
        else:
            print('Admin user already exists')