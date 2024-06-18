import os

from celery import Celery

# Установить настройки по умолчанию из Django-проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загружать задачи из всех зарегистрированных приложений Django
app.autodiscover_tasks()