from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Lesson
from users.services import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def send_confirm_email(self, subject, message):
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [f'{self.email}'],
            fail_silently=False,
        )


class Payment(models.Model):

    METHODS = (
        ("CASH", "Наличные"),
        ("NON_CASH", "Безнал")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateTimeField(auto_now=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=10, default="NON_CASH", choices=METHODS, verbose_name="Способ оплаты")
    payment_status = models.CharField(default='unpaid', verbose_name='Статус оплаты')
    payment_url = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)
    session_id = models.CharField(max_length=255, verbose_name='id платежной сессии', **NULLABLE)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("date",)

    def __str__(self):
        return (f'Платёж {self.payment_amount} от {self.user} способ оплаты {self.payment_method} '
                f'за {self.course if self.course else self.lesson}')
