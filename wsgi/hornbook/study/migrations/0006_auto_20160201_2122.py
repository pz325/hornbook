# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0005_auto_20160201_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='display',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
