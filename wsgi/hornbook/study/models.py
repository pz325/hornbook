from django.db import models
from django.contrib.auth.models import User
from lexicon.models import Hanzi
from django.contrib import admin
import django.utils.timezone

import leitner

'''
Leitner system, a spaced repetition method.
refer to http://en.wikipedia.org/wiki/Leitner_system
Here we implements the Example Two
'''

STUDY_RECORD_STATUS = (
    ('N', 'New'),
    ('S', 'Studying'),
    ('G', 'Grasped'),
    )


class StudyRecord(models.Model):
    user = models.ForeignKey(User, editable=False, db_index=True, related_name='study_records')
    study_date = models.DateTimeField(auto_now=True)
    revise_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STUDY_RECORD_STATUS, default='N')
    repeat_count = models.PositiveSmallIntegerField(default=0)
    forget_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True


class LeitnerStudyRecord(StudyRecord):
    leitner_deck = models.CharField(max_length=1, choices=leitner.DECK_TYPE, default='C', db_index=True)

    class Meta:
        abstract = True


class HanziStudyRecord(LeitnerStudyRecord):
    hanzi = models.ForeignKey(Hanzi, editable=False, db_index=True)


class HanziStudyCount(models.Model):
    user = models.OneToOneField(User, editable=False, db_index=True, related_name='study_counts', primary_key=True)
    count = models.PositiveSmallIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)


admin.site.register(HanziStudyRecord)
admin.site.register(HanziStudyCount)
