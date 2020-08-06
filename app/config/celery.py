from __future__ import absolute_import, unicode_literals

import os
import uuid
from time import sleep

from celery import Celery, shared_task

# set the default Django settings module for the 'celery' program.
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('config', broker='redis://localhost/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@shared_task
def create_users_send_mail_async(mail, **kwargs):
    from django.core.mail import EmailMessage
    email_var = mail
    subject = 'Django를 통해 발송한 메일'
    message = 'Django 를 통해 발송한 메일 입니다.'
    email = EmailMessage(subject, message, to=[email_var])
    # email.send()
