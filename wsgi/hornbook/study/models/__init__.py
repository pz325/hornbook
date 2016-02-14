#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from study import HanziStudyRecord
from study import HanziStudyCount
from category import Category


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
    read_hanzi = Category.objects.create(user=user, display='read_hanzi')
    write_hanzi = Category.objects.create(user=user, display='write_hanzi')
    chinese_poem = Category.objects.create(user=user, display='chinese_poem')
    # add count
    HanziStudyCount.objects.create(user=user, category=read_hanzi, count=1)
    HanziStudyCount.objects.create(user=user, category=write_hanzi, count=1)
    HanziStudyCount.objects.create(user=user, category=chinese_poem, count=1)
