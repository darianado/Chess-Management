# Generated by Django 3.2.5 on 2021-11-19 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_user_gravatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gravatar',
        ),
    ]
