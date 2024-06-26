# Generated by Django 5.0.6 on 2024-06-14 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0003_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="amount",
            field=models.PositiveIntegerField(default=1000, verbose_name="Цена курса"),
        ),
        migrations.AddField(
            model_name="lesson",
            name="amount",
            field=models.PositiveIntegerField(default=200, verbose_name="Цена урока"),
        ),
    ]
