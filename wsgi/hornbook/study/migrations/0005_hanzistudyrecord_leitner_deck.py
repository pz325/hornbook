# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0004_auto_20151109_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='hanzistudyrecord',
            name='leitner_deck',
            field=models.CharField(default=b'C', max_length=1, db_index=True, choices=[(b'C', b'Current'), (b'0', b'Progress_0'), (b'1', b'Progress_1'), (b'2', b'Progress_2'), (b'3', b'Progress_3'), (b'4', b'Progress_4'), (b'5', b'Progress_5'), (b'6', b'Progress_6'), (b'7', b'Progress_7'), (b'8', b'Progress_8'), (b'9', b'Progress_9'), (b'R', b'Retired')]),
        ),
    ]
