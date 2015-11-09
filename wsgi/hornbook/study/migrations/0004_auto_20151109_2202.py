# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study', '0003_auto_20151010_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('user', models.ForeignKey(related_name='categories', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='hanzistudyrecord',
            name='leitner_deck',
        ),
        migrations.AddField(
            model_name='hanzistudyrecord',
            name='category',
            field=models.ForeignKey(blank=True, editable=False, to='study.Category', null=True),
        ),
    ]
