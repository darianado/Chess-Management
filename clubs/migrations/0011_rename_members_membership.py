# Generated by Django 3.2.5 on 2021-12-07 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0010_alter_events_action'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Members',
            new_name='Membership',
        ),
    ]
