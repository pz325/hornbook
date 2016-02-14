# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0007_auto_20160207_2336'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StudySessionContentLog',
        ),
        migrations.DeleteModel(
            name='StudySessionResultLog',
        ),
    ]
