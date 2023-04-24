# Generated by Django 4.2a1 on 2023-04-15 10:48

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc

import mwk.modules.main.helpers.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
                ),
                (
                    'bio',
                    models.TextField(
                        blank=True,
                        max_length=100,
                        verbose_name='Status'
                    ),
                ),
                (
                    'avatar',
                    models.ImageField(
                        blank=True,
                        default='default/default.png',
                        upload_to=mwk.modules.main.helpers.helpers.PathAndRenameDate(
                            'photos/avatars/'
                        ),
                        verbose_name='Avatar',
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='profile',
                        related_query_name='profile',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='User',
                    ),
                ),
                (
                    'birthday',
                    models.DateField(
                        default=datetime.datetime(2022, 1, 1, 18, 00, 00, tzinfo=utc),
                        null=True,
                        verbose_name='Birthday',
                    ),
                )
            ],
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
