import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'shop.settings')

import django
django.setup()

from shop.tasks import email_sender


email_sender()
