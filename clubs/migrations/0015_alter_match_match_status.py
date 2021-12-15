# Generated by Django 3.2.5 on 2021-12-15 02:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0014_alter_tournament_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='match_status',
            field=models.IntegerField(choices=[(1, "Match hasn't been played yet"), (2, 'Match was drawn'), (3, 'Player A won'), (4, 'Player B won')], default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)]),
        ),
    ]
