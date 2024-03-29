# Generated by Django 3.2.5 on 2021-11-27 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0006_auto_20211119_2310'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='members',
            name='member of a club only once',
        ),
        migrations.AddConstraint(
            model_name='members',
            constraint=models.UniqueConstraint(fields=('club', 'user'), name='Member of a club only once'),
        ),
        migrations.AddConstraint(
            model_name='members',
            constraint=models.UniqueConstraint(condition=models.Q(('role', 1)), fields=('club',), name='Every club has at most 1 owner'),
        ),
    ]
