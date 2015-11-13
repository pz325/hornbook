# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0010_auto_20151113_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hanzistudycount',
            name='user',
            field=models.ForeignKey(related_name='study_counts', editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
