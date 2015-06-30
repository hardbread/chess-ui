# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_time_st', models.TimeField(verbose_name=b'Start time')),
                ('game_time_end', models.TimeField(verbose_name=b'End time')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('rating', models.DecimalField(max_digits=7, decimal_places=3, db_index=True)),
                ('birthday', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=b'0', editable=False, choices=[(b'1', b'Win'), (b'0.5', b'Draw'), (b'0', b'Loss')])),
                ('match', models.ForeignKey(related_name='score_match', to='api.Match')),
                ('player', models.ForeignKey(related_name='score_player', to='api.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match', models.ForeignKey(related_name='team_match', to='api.Match')),
                ('player_1', models.ForeignKey(related_name='team_player_1', to='api.Player')),
                ('player_2', models.ForeignKey(related_name='team_player_2', to='api.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
                ('winner', models.ForeignKey(related_name='tournament_winner', blank=True, to='api.Player', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('first_name', 'last_name', 'birthday')]),
        ),
        migrations.AlterIndexTogether(
            name='player',
            index_together=set([('first_name', 'last_name', 'rating')]),
        ),
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(related_name='match_tournament', to='api.Tournament'),
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(related_name='match_winner', blank=True, to='api.Player', null=True),
        ),
        migrations.AlterIndexTogether(
            name='tournament',
            index_together=set([('start_date', 'end_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('player_1', 'player_2', 'match')]),
        ),
        migrations.AlterIndexTogether(
            name='match',
            index_together=set([('game_time_st', 'game_time_end')]),
        ),
    ]
