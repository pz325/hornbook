# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0006_auto_20160201_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('font_size', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.RemoveField(
            model_name='category',
            name='unique_name',
        ),
        migrations.AlterField(
            model_name='category',
            name='display',
            field=models.CharField(default=b'display', max_length=200),
        ),
        migrations.AddField(
            model_name='category',
            name='card',
            field=models.ForeignKey(to='study.Card', null=True),
        ),
    ]
