# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lexicon', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unique_name', models.CharField(unique=True, max_length=200, editable=False, db_index=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('user', models.ForeignKey(related_name='categories', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HanziStudyCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveSmallIntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(editable=False, to='study.Category')),
                ('user', models.ForeignKey(related_name='study_counts', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HanziStudyRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('study_date', models.DateTimeField(auto_now=True)),
                ('revise_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'New'), (b'S', b'Studying'), (b'G', b'Grasped')])),
                ('repeat_count', models.PositiveSmallIntegerField(default=0)),
                ('forget_count', models.PositiveSmallIntegerField(default=0)),
                ('leitner_deck', models.CharField(default=b'C', max_length=1, db_index=True, choices=[(b'C', b'Current'), (b'0', b'Progress_0'), (b'1', b'Progress_1'), (b'2', b'Progress_2'), (b'3', b'Progress_3'), (b'4', b'Progress_4'), (b'5', b'Progress_5'), (b'6', b'Progress_6'), (b'7', b'Progress_7'), (b'8', b'Progress_8'), (b'9', b'Progress_9'), (b'R', b'Retired')])),
                ('category', models.ForeignKey(editable=False, to='study.Category')),
                ('hanzi', models.ForeignKey(editable=False, to='lexicon.Hanzi')),
                ('user', models.ForeignKey(related_name='study_records', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
