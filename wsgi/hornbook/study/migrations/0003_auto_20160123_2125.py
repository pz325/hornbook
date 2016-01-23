# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_studysessioncontentlog_studysessionresultlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studysessioncontentlog',
            name='contents',
        ),
        migrations.AddField(
            model_name='studysessioncontentlog',
            name='current_deck_contents',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='studysessioncontentlog',
            name='progress_deck_contents',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='studysessioncontentlog',
            name='retired_deck_contents',
            field=models.TextField(blank=True),
        ),
    ]
