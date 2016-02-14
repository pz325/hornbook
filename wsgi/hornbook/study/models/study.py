from django.db import models
from django.contrib.auth.models import User
from category import Category
from lexicon.models import Hanzi
import leitner


class StudyRecord(models.Model):
    user = models.ForeignKey(User, editable=False, db_index=True, related_name='study_records')
    study_date = models.DateTimeField(auto_now=True)
    revise_date = models.DateTimeField(auto_now=True)
    repeat_count = models.PositiveSmallIntegerField(default=0)
    forget_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True


class LeitnerStudyRecord(StudyRecord):
    leitner_deck = models.CharField(max_length=1, choices=leitner.DECK_TYPE, default='C', db_index=True)

    class Meta:
        abstract = True


class CategorisedLeitnerStudyRecord(LeitnerStudyRecord):
    category = models.ForeignKey(Category, editable=False, db_index=True)

    class Meta:
        abstract = True


class HanziStudyRecord(CategorisedLeitnerStudyRecord):
    hanzi = models.ForeignKey(Hanzi, editable=False, db_index=True)

    def __unicode__(self):
        return '.'.join([self.user.username, self.category.name, self.hanzi.content])


class HanziStudyCount(models.Model):
    user = models.ForeignKey(User, editable=False, db_index=True, related_name='study_counts')
    count = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(Category, editable=False, db_index=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '.'.join([self.user.username, self.category.name, str(self.count)])
