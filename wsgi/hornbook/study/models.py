#!/usr/bin/python
# -*- coding: utf-8 -*-

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


class StudySessionContentLog(models.Model):
    date = models.DateTimeField(auto_now=True)
    session_count = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=200)
    contents = models.TextField()


class StudySessionResultLog(models.Model):
    date = models.DateTimeField(auto_now=True)
    session_count = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=200)
    grasped_contents = models.TextField()
    new_contents = models.TextField()


class Category(models.Model):
    unique_name = models.CharField(max_length=200, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, editable=False, db_index=True, related_name='categories')

    def save(self, *args, **kwargs):
        self.unique_name = '_'.join([self.name, self.user.username])
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.unique_name


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


import re
from datetime import datetime
import codecs


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


def importGAEData():
    '''
    need the following (in iPython) before run this:
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")
    '''
    user = User.objects.get(username='xinrong')
    category = Category.objects.get(user=user, name='read_hanzi')
    filename = '../../gae.data'
    for line in codecs.open(filename, 'rb', 'utf-8'):
        if not re.match('\s+', line):
            _, deck, forget_times, hanzi, last_study_date, last_study_time, level, user_id, _ = re.split('\s+', line)

            if deck == 'P':
                deck = 'R'
            study_status = 'S'
            if deck == 'R':
                study_status = 'G'
            if deck == 'C':
                study_status = 'N'

            if (user_id == '5838406743490560'):
                leitner_record = {
                    'deck': deck,
                    'forget_times': int(forget_times),
                    'hanzi': hanzi,
                    'last_study_datetime': datetime.strptime(last_study_date + ' ' + last_study_time, '%Y-%m-%d %H:%M:%S')
                    }

                print(leitner_record)
                hanzi_instance, _ = Hanzi.objects.get_or_create(content=hanzi)
                print(hanzi_instance)

                HanziStudyRecord.objects.create(
                    user=user,
                    category=category,
                    hanzi=hanzi_instance,
                    leitner_deck=leitner_record['deck'],
                    forget_count=leitner_record['forget_times'],
                    repeat_count=leitner_record['forget_times'],
                    study_date=leitner_record['last_study_datetime'],
                    revise_date=leitner_record['last_study_datetime'],
                    status=study_status
                    )
    print('done')
