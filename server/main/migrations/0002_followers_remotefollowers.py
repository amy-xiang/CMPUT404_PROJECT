# Generated by Django 3.1.6 on 2021-03-23 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='followers',
            name='remoteFollowers',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
