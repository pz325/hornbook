# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_auto_20150923_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hanzistudycount',
            name='id',
        ),
        migrations.RemoveField(
            model_name='hanzistudyrecord',
            name='leitner_level',
        ),
        migrations.AlterField(
            model_name='hanzistudycount',
            name='user',
            field=models.OneToOneField(related_name='study_counts', primary_key=True, serialize=False, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hanzistudyrecord',
            name='hanzi',
            field=models.ForeignKey(editable=False, to='lexicon.Hanzi'),
        ),
        migrations.AlterField(
            model_name='hanzistudyrecord',
            name='leitner_deck',
            field=models.CharField(default=b'C', max_length=1, db_index=True, choices=[(b'C', b'Current'), (b'0', b'Progress_0'), (b'1', b'Progress_1'), (b'2', b'Progress_2'), (b'3', b'Progress_3'), (b'4', b'Progress_4'), (b'5', b'Progress_5'), (b'6', b'Progress_6'), (b'7', b'Progress_7'), (b'8', b'Progress_8'), (b'9', b'Progress_9'), (b'R', b'Retired')]),
        ),
        migrations.AlterField(
            model_name='hanzistudyrecord',
            name='revise_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='hanzistudyrecord',
            name='status',
            field=models.CharField(default=b'N', max_length=1, choices=[(b'N', b'New'), (b'S', b'Studying'), (b'G', b'Grasped')]),
        ),
        migrations.AlterField(
            model_name='hanzistudyrecord',
            name='study_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
