from django.db import models
from django.contrib.auth.models import User
from lexicon.models import Hanzi
from django.contrib import admin
import django.utils.timezone

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

LEITNER_DECK_TYPE = (
    ('C', 'Current'),
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('R', 'Retired'),
    ('P', 'Permanent'),
    )

LEITNER_LEVEL = (
    (0, 'Level 0'),
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3, 'Level 3'),
    (4, 'Level 4'),
    (5, 'Level 5'),
    (6, 'Level 6'),
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
    leitner_deck = models.CharField(max_length=1, choices=LEITNER_DECK_TYPE, default='C', db_index=True)
    leitner_level = models.PositiveSmallIntegerField(choices=LEITNER_LEVEL, default=0, db_index=True)

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
