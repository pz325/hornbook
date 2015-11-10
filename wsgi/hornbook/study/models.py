from django.db import models
from django.contrib.auth.models import User
from lexicon.models import Hanzi
from django.contrib import admin
import django.utils.timezone
from django.contrib.auth.decorators import login_required

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


class Category(models.Model):
    unique_name = models.CharField(max_length=200, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, editable=False, db_index=True, related_name='categories')

    def save(self, *args, **kwargs):
        self.unique_name = '_'.join([self.name, self.user.username])
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


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


class CategorisedLeitnerStudyRecord(LeitnerStudyRecord):
    category = models.ForeignKey(Category, editable=False, db_index=True)  # todo, revert to db_index=True

    class Meta:
        abstract = True


class HanziStudyRecord(CategorisedLeitnerStudyRecord):
    hanzi = models.ForeignKey(Hanzi, editable=False, db_index=True)


class HanziStudyCount(models.Model):
    user = models.OneToOneField(User, editable=False, db_index=True, related_name='study_counts', primary_key=True)
    count = models.PositiveSmallIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)


admin.site.register(HanziStudyRecord)
admin.site.register(HanziStudyCount)
admin.site.register(Category)


def populateDefaultCategory(username):
    user = User.objects.get(username=username)
    category = Category.objects.filter(user=user)[0]
    for r in HanziStudyRecord.objects.filter(user=user):
        r.category = category
        r.save()
