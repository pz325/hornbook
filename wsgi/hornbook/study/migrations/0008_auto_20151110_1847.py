# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0007_auto_20151109_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hanzistudyrecord',
            name='category',
            field=models.ForeignKey(editable=False, to='study.Category'),
        ),
    ]
