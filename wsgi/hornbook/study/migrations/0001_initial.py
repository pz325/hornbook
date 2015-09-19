# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lexicon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HanziStudyCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveSmallIntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HanziStudyRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('study_date', models.DateTimeField()),
                ('revise_date', models.DateTimeField()),
                ('status', models.CharField(max_length=1, choices=[(b'N', b'New'), (b'S', b'Studying'), (b'G', b'Grasped')])),
                ('repeat_count', models.PositiveSmallIntegerField(default=0)),
                ('forget_count', models.PositiveSmallIntegerField(default=0)),
                ('leitner_deck', models.CharField(default=b'C', max_length=1, db_index=True, choices=[(b'C', b'Current'), (b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5'), (b'6', b'6'), (b'7', b'7'), (b'8', b'8'), (b'9', b'9'), (b'R', b'Retired'), (b'P', b'Permanent')])),
                ('leitner_level', models.PositiveSmallIntegerField(default=0, db_index=True, choices=[(0, b'Level 0'), (1, b'Level 1'), (2, b'Level 2'), (3, b'Level 3'), (4, b'Level 4'), (5, b'Level 5'), (6, b'Level 6')])),
                ('hanzi', models.ForeignKey(to='lexicon.Hanzi')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
