# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0009_studysessioncontentlog_studysessionresultlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='num_retired',
            field=models.PositiveSmallIntegerField(default=10),
        ),
    ]
