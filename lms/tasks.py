from datetime import datetime, timedelta, timezone
import pytz
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from loguru import logger

from lms.models import Course, Subscription
from users.models import User


logger.add("log.log", format="{time} {level} {message}", level="INFO", rotation="1 week")


@shared_task
def send_email_about_update_course(course_id):
    course = Course.objects.get(pk=course_id)
    subscribers = Subscription.objects.get(course=course_id)

    send_mail(
        subject=f'Курс {course} обновлен',
        message=f'Курс {course},на который вы подписаны обновлён',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[subscribers.user.email]
    )
    logger.info(f'Курс {course.name} обновлён')


@shared_task
def check_user():
    active_users = User.objects.filter(is_active=True, is_superuser=False, last_login__isnull=False)
    now_time = datetime.now()
    for user in active_users:
        if user.last_login:
            if now_time - user.last_login > timedelta(days=10):
                user.is_active = False
                user.save()
                logger.info(f"Пользователь {user} заблокирован за пассивность")
