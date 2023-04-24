# Generated by Django 4.2a1 on 2023-04-19 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_create_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(
                related_name='following',
                through='authentication.Contact',
                to='authentication.profile',
            ),
        ),
    ]
