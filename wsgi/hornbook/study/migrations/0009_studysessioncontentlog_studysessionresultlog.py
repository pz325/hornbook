# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0008_auto_20160208_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudySessionContentLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('session_count', models.PositiveSmallIntegerField(default=0)),
                ('category', models.CharField(max_length=200)),
                ('current_deck_contents', models.TextField(blank=True)),
                ('progress_deck_contents', models.TextField(blank=True)),
                ('retired_deck_contents', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudySessionResultLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('session_count', models.PositiveSmallIntegerField(default=0)),
                ('category', models.CharField(max_length=200)),
                ('grasped_contents', models.TextField()),
                ('new_contents', models.TextField()),
            ],
        ),
    ]
