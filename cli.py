import os

import sys
import django
from django.conf import settings
from server import views

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "server"))

def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default":{
                "ENGINE":"django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(
            "server",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # print(sys.argv, "11111111111111")
    execute_from_command_line(sys.argv)

boot_django()