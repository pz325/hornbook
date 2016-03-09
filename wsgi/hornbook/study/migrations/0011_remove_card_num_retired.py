# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0010_card_num_retired'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='num_retired',
        ),
    ]
