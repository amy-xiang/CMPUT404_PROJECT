# Generated by Django 3.1.6 on 2021-02-19 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inbox', '0003_auto_20210219_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbox',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
