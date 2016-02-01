#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from lexicon.models import Hanzi
from django.contrib import admin
import leitner
'''
Leitner system, a spaced repetition method.
refer to http://en.wikipedia.org/wiki/Leitner_system
Here we implements the Example Two
'''


class StudySessionContentLog(models.Model):
    date = models.DateTimeField(auto_now=True)
    session_count = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=200)
    current_deck_contents = models.TextField(blank=True)
    progress_deck_contents = models.TextField(blank=True)
    retired_deck_contents = models.TextField(blank=True)


class StudySessionResultLog(models.Model):
    date = models.DateTimeField(auto_now=True)
    session_count = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=200)
    grasped_contents = models.TextField()
    new_contents = models.TextField()


class Category(models.Model):
    '''
    unique_name filed is the index, so to assure the uniqueness of "category name and user name".
    '''
    unique_name = models.CharField(max_length=200, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, editable=False, db_index=True, related_name='categories')
    display = models.CharField(max_length=200, blank=True)
    num_retired = models.PositiveSmallIntegerField(default=10)

    def save(self, *args, **kwargs):
        self.unique_name = '_'.join([self.name, self.user.username])
        if not self.display:
            self.display = self.name
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.display + ': ' + self.unique_name


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

admin.site.register(HanziStudyRecord)
admin.site.register(HanziStudyCount)
admin.site.register(Category)


def populateDefaultCategory(username):
    user = User.objects.get(username=username)
    category = Category.objects.filter(user=user)[0]
    for r in HanziStudyRecord.objects.filter(user=user):
        r.category = category
        r.save()


def populateCategoryToCount(username):
    user = User.objects.get(username=username)
    category = Category.objects.filter(user=user)[0]
    for r in HanziStudyCount.objects.filter(user=user):
        r.category = category
        r.save()


def setupHornbookForUser(username):
    # add user xinrong
    user = User.objects.get(username=username)
    # add category
    read_hanzi = Category.objects.create(user=user, name='read_hanzi')
    write_hanzi = Category.objects.create(user=user, name='write_hanzi')
    chinese_poem = Category.objects.create(user=user, name='chinese_poem')
    # add count
    read_hanzi_count = HanziStudyCount.objects.create(user=user, category=read_hanzi, count=1)
    write_hanzi_count = HanziStudyCount.objects.create(user=user, category=write_hanzi, count=1)
    chinese_poem_count = HanziStudyCount.objects.create(user=user, category=chinese_poem, count=1)
