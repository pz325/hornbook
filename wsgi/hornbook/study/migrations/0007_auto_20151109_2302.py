# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0006_auto_20151109_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='unique_name',
            field=models.CharField(default='d', unique=True, max_length=200, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([]),
        ),
    ]
