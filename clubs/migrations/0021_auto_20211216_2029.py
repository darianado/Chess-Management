# Generated by Django 3.2.5 on 2021-12-16 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0020_alter_tournament_coorganisers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={},
        ),
        migrations.RemoveField(
            model_name='participant',
            name='score',
        ),
    ]
