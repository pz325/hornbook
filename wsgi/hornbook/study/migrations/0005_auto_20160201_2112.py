# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0004_remove_hanzistudyrecord_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='display',
            field=models.CharField(default=b'display', max_length=200),
        ),
        migrations.AddField(
            model_name='category',
            name='num_retired',
            field=models.PositiveSmallIntegerField(default=10),
        ),
    ]
