# Generated by Django 3.1.6 on 2021-03-23 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contentType',
            field=models.CharField(choices=[('Text', (('text/markdown', 'markdown'), ('text/plain', 'plain'), ('text/html', 'html'))), ('Encoded Text', (('application/base64', 'base64'),)), ('Image', (('image/png;base64', '.png'), ('image/jpeg;base64', '.jpg')))], default='text/markdown', max_length=18),
        ),
    ]
