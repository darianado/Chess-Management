# Generated by Django 3.2.5 on 2021-12-05 17:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0010_alter_events_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_active', models.BooleanField(default=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.members')),
            ],
            options={
                'ordering': ['-score'],
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=260)),
                ('deadline', models.DateTimeField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.club')),
                ('coorganisers', models.ManyToManyField(to='clubs.Members')),
                ('organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organiser', to='clubs.members')),
                ('participants', models.ManyToManyField(related_name='participants', through='clubs.Participant', to='clubs.Members')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.tournament'),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_status', models.IntegerField(choices=[(1, 'Not Played'), (2, 'Drawn'), (3, 'Won A'), (4, 'Won B')], default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('playerA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playerA', to='clubs.participant')),
                ('playerB', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playerB', to='clubs.participant')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.tournament')),
            ],
        ),
        migrations.AddConstraint(
            model_name='match',
            constraint=models.CheckConstraint(check=models.Q(('playerA', django.db.models.expressions.F('playerB')), _negated=True), name='players_diff'),
        ),
    ]
