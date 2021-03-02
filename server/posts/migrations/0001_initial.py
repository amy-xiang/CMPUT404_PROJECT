# Generated by Django 3.1.6 on 2021-03-02 22:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source', models.URLField(blank=True, help_text='last location/url where we got this post')),
                ('origin', models.URLField(blank=True, help_text='original location/url')),
                ('description', models.CharField(blank=True, max_length=250)),
                ('contentType', models.CharField(choices=[('Text', (('text/markdown', 'markdown'), ('text/plain', 'plain'), ('text/html', 'html'))), ('Encoded Text', (('application/base64', 'base64'),)), ('Image', (('image/png;base64', '.png'), ('image/jpeg;base64', '.jpg')))], default='text/markdown', max_length=18)),
                ('content', models.TextField(blank=True, null=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('size', models.PositiveIntegerField(default=0)),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'Public'), ('FRIENDS', 'Friends')], default='PUBLIC', max_length=10)),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(blank=True, to='posts.Category')),
            ],
        ),
    ]
