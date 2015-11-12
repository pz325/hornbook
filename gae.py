#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import re
from datetime import datetime


for line in codecs.open('gae.data', 'rb', 'utf-8'):
    if not re.match('\s+', line):
        _, deck, forget_times, hanzi, last_study_date, last_study_time, level, user_id, _ = re.split('\s+', line)
        if (user_id == '5838406743490560'):
            leitner_record = {
                'deck': deck,
                'forget_times': forget_times,
                'hanzi': hanzi,
                'last_study_datetime': datetime.strptime(last_study_date + ' ' + last_study_time, '%Y-%m-%d %H:%M:%S')
                }
            print(leitner_record)
