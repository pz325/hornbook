# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hanzistudyrecord',
            name='user',
            field=models.ForeignKey(related_name='study_records', editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
