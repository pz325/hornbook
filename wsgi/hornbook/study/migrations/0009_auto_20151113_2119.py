# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0008_auto_20151110_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='hanzistudycount',
            name='category',
            field=models.ForeignKey(default=1, editable=False, to='study.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hanzistudycount',
            name='id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
