from django.db import models

from config import settings
from services import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    preview = models.ImageField(upload_to='lms/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец',
                              related_name='owner_course')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    preview = models.ImageField(upload_to='lms/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='course')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец',
                              related_name='owner_lesson', **NULLABLE)

    def __str__(self):
        return f'{self.name}, курс {self.course}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.CASCADE)

    def __str__(self):
        return f'Пользователь с id {self.user} подписан на курс {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
