# Generated by Django 3.2.5 on 2021-12-15 21:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0017_alter_match_match_round'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='capacity',
            field=models.IntegerField(default=16, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(16)]),
        ),
    ]
