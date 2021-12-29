from __future__ import absolute_import,unicode_literals

import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','familyalbum.settings')

app = Celery('familyalbum')
app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": "CERT_NONE"}

app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)