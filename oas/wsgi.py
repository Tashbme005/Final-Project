"""
WSGI config for oas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import shutil
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oas.settings')

application = get_wsgi_application()
app = application

if os.environ.get('VERCEL') == '1':
    from django.conf import settings
    from django.core.management import call_command

    db = settings.DATABASES['default']
    if db['ENGINE'].endswith('sqlite3'):
        shipped = Path(__file__).resolve().parent.parent / 'db.sqlite3'
        live = Path(db['NAME'])
        live.parent.mkdir(parents=True, exist_ok=True)
        if shipped.exists():
            shutil.copyfile(shipped, live)
    call_command('migrate', interactive=False, verbosity=0)
