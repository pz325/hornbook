# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from study.models import HanziStudyCount
from study.models import HanziStudyRecord
from study.models import Category
from study.models import Card
from lexicon.models import Hanzi
from django.contrib.auth.models import User

from leitner import is_last_number_on_deck
from leitner import to_review
from leitner import decks_to_review

import json
from random import randint
import unittest






class HanziStudyCountViewSetTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = _create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)

        self.category = _create_one_Category_instance(self.user, 'category')

        another_user = _create_one_User_instance('another_user')
        another_category = _create_one_Category_instance(another_user, 'another_category')
        _create_one_HanziStudyCount_instance(another_user, another_category, 10)

    def test_create_response_404_when_without_category_parameter(self):
        # arrange
        count = 3
        data = {'count': count}
        # act
        url = reverse('hanzistudycount-list')
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        # arrange
        count = 3
        data = {'count': count, 'category': self.category.name}

        # act
        url = reverse('hanzistudycount-list')
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HanziStudyCount.objects.filter(user=self.user).count(), 1)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).category.unique_name, self.category.unique_name)

    def test_list_without_category_parameter(self):
        # arrange
        count = 3
        categoryA = _create_one_Category_instance(self.user, 'categoryA')
        categoryB = _create_one_Category_instance(self.user, 'categoryB')

        _create_one_HanziStudyCount_instance(self.user, categoryA, count)
        _create_one_HanziStudyCount_instance(self.user, categoryB, count)

        # act
        url = reverse('hanzistudycount-list')
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list(self):
        # arrange
        count = 3
        _create_one_HanziStudyCount_instance(self.user, self.category, count)

        # act
        url = reverse('hanzistudycount-list')
        url += '?category={category}'.format(category=self.category.name)
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['count'], count)

    def test_get_one(self):
        '''
        pk -- HanziStudyCount id
        '''
        # arrange
        count = 3
        study_count = _create_one_HanziStudyCount_instance(self.user, self.category, count)

        # act
        url = reverse('hanzistudycount-detail', args=[study_count.id])
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], count)
        self.assertEqual(response.data['category'], self.category.name)

    def test_put_one(self):
        '''
        pk -- HanziStudyCount id
        '''
        # arrange
        count = 3
        study_count = _create_one_HanziStudyCount_instance(self.user, self.category, count)

        # act
        count = 6
        data = {'count': count}
        url = reverse('hanzistudycount-detail', args=[study_count.id])
        response = self.client.put(url, data=data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.filter(user=self.user).count(), 1)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).category.unique_name, self.category.unique_name)

    def test_delete_one(self):
        '''
        pk -- HanziStudyCount id
        '''
        # arrange
        count = 3
        study_count = _create_one_HanziStudyCount_instance(self.user, self.category, count)

        # act
        url = reverse('hanzistudycount-detail', args=[study_count.id])
        response = self.client.delete(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HanziStudyCount.objects.filter(user=self.user).count(), 0)


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = _create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)

        self.category = _create_one_Category_instance(self.user, 'category')

        another_user = _create_one_User_instance('another_user')
        another_category = _create_one_Category_instance(another_user, 'another_category')
        _create_one_HanziStudyCount_instance(another_user, another_category, 10)

        hanzi = u'王'
        category = _create_one_Category_instance(another_user, 'category_for_another_user')
        _create_one_HanziStudyRecord_instance(another_user, category, hanzi)

    def test_list_User(self):
        # arrange
        count = 3
        _create_one_HanziStudyCount_instance(self.user, self.category, count)
        hanzi = u'风'
        _create_one_HanziStudyRecord_instance(self.user, self.category, hanzi)

        # act
        url = reverse('user-list')
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result_data = response.data['results']
        self.assertEqual(len(result_data), 1)
        self.assertEqual(result_data[0]['username'], self.user.username)
        self.assertEqual(len(result_data[0]['study_records']), 1)
        self.assertEqual(result_data[0]['study_records'][0], 'http://testserver' + reverse('hanzistudyrecord-detail', args=[2]))

    def test_get_one_User(self):
        # arrange
        count = 3
        _create_one_HanziStudyCount_instance(self.user, self.category, count)
        hanzi = u'风'
        _create_one_HanziStudyRecord_instance(self.user, self.category, hanzi)

        # act
        url = reverse('user-detail', args=[1])
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['study_records']), 1)
        self.assertEqual(response.data['study_records'][0], 'http://testserver' + reverse('hanzistudyrecord-detail', args=[2]))


class HanziStudyRecordViewSetTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = _create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)
        self.category = _create_one_Category_instance(self.user, 'category')

        another_user = _create_one_User_instance('another_user')
        another_category = _create_one_Category_instance(another_user, 'category_for_another_user')
        _create_one_HanziStudyRecord_instance(another_user, another_category, u'王')

    def test_list_without_catetory_parameter(self):
        # arrange
        hanzi = u'东'
        category = _create_one_Category_instance(self.user, 'categoryA')
        _create_one_HanziStudyRecord_instance(self.user, category, hanzi)

        hanzi = u'南'
        category = _create_one_Category_instance(self.user, 'categoryB')
        _create_one_HanziStudyRecord_instance(self.user, category, hanzi)

        # act
        url = reverse('hanzistudyrecord-list')
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        pass

    def test_list(self):
        # arrange
        hanzis = [u'东', u'南']
        for h in hanzis:
            _create_one_HanziStudyRecord_instance(self.user, self.category, h)

        # act
        url = reverse('hanzistudyrecord-list') + '?category={category}'.format(category=self.category.name)
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_reponse_400_when_without_category_parameter(self):
        # arrange
        url = reverse('hanzistudyrecord-list')
        hanzi = u'东'
        data = {'hanzi': hanzi}

        # act
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create(self):
        # arrange
        url = reverse('hanzistudyrecord-list')
        hanzi = u'东'
        data = {'hanzi': hanzi, 'category': self.category.name}

        # act
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HanziStudyRecord.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Hanzi.objects.filter(content=hanzi).count(), 1)
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, category=self.category).hanzi, Hanzi.objects.get(content=hanzi))

    def test_get_one(self):
        '''
        pk -- HanziStudyRecord id
        '''
        # arrange
        hanzi = u'东'
        hanzi_study_record_instance = _create_one_HanziStudyRecord_instance(self.user, self.category, hanzi)

        # act
        url = reverse('hanzistudyrecord-detail', args=[hanzi_study_record_instance.id])
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['hanzi'], hanzi)

    def test_put_one(self):
        '''
        pk -- HanziStudyRecord id
        '''
        # arrange
        hanzi = u'东'
        hanzi_study_record_instance = _create_one_HanziStudyRecord_instance(self.user, self.category, hanzi)

        # act
        hanzi = u'王'
        data = {'hanzi': hanzi, 'category': self.category.name}
        url = reverse('hanzistudyrecord-detail', args=[hanzi_study_record_instance.id])
        response = self.client.put(url, data=data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyRecord.objects.filter(user=self.user).count(), 1)
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user), hanzi_study_record_instance)

    def test_delete_one(self):
        '''
        pk -- HanziStudyRecord id
        '''
        # arrange
        hanzi = u'东'
        hanzi_study_record_instance = _create_one_HanziStudyRecord_instance(self.user, self.category, hanzi)

        # act
        url = reverse('hanzistudyrecord-detail', args=[hanzi_study_record_instance.id])
        response = self.client.delete(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HanziStudyRecord.objects.filter(user=self.user).count(), 0)

    def test_get_leitner_record_response_404_without_category_parameter(self):
        # arrange
        _create_one_leitner_record(self.user, self.category.name, u'东', 'C')
        _create_one_leitner_record(self.user, self.category.name, u'南', '1')
        _create_one_leitner_record(self.user, self.category.name, u'西', '3')
        _create_one_HanziStudyCount_instance(self.user, self.category, 1)

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_leitner_record(self):
        # arrange
        _create_one_leitner_record(self.user, self.category.name, u'东', 'C')
        _create_one_leitner_record(self.user, self.category.name, u'南', '1')
        _create_one_leitner_record(self.user, self.category.name, u'西', '3')
        _create_one_HanziStudyCount_instance(self.user, self.category, 1)

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        url += '?category={category}'.format(category=self.category.name)
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_leitner_record_with_num_retired(self):
        # arrange
        retired_hanzis = [u'北', u'春', u'夏', u'冬']
        _create_one_leitner_record(self.user, self.category.name, u'东', 'C')
        _create_one_leitner_record(self.user, self.category.name, u'南', '1')
        _create_one_leitner_record(self.user, self.category.name, u'西', '3')
        for h in retired_hanzis:
            _create_one_leitner_record(self.user, self.category.name, h, 'R')
        _create_one_HanziStudyCount_instance(self.user, self.category, 1)

        # act
        num_retired = 2
        url = reverse('hanzistudyrecord-list') + '/leitner_record?num_retired={num_retired}'.format(num_retired=num_retired)
        url += '&category={category}'.format(category=self.category.name)
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # two from deck R

    def test_set_leitner_record_response_404_when_without_category_parameter(self):
        # arrange
        retired_hanzis = [u'北', u'春', u'夏', u'冬']
        _create_one_leitner_record(self.user, self.category.name, u'东', 'C')
        _create_one_leitner_record(self.user, self.category.name, u'南', '1')
        _create_one_leitner_record(self.user, self.category.name, u'西', '2')
        for h in retired_hanzis:
            _create_one_leitner_record(self.user, self.category.name, h, 'R')
        _create_one_HanziStudyCount_instance(self.user, self.category, 1)

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        data = {
            'grasped_hanzi': json.dumps([u'东', u'西', u'冬']),   # 东 -> deck 1, 西 -> deck R, 冬 -> deck R
            'new_hanzi': json.dumps([u'李', u'南'])        # 南 -> deck C, new Hanzi, 李 -> deck C
        }

        response = self.client.post(url, data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_leitner_record(self):
        # arrange
        retired_hanzis = [u'北', u'春', u'夏', u'冬']
        _create_one_leitner_record(self.user, self.category.name, u'东', 'C')
        _create_one_leitner_record(self.user, self.category.name, u'南', '1')
        _create_one_leitner_record(self.user, self.category.name, u'西', '2')
        for h in retired_hanzis:
            _create_one_leitner_record(self.user, self.category.name, h, 'R')
        _create_one_HanziStudyCount_instance(self.user, self.category, 1)

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        data = {
            'category': self.category.name,
            'grasped_hanzi': json.dumps([u'东', u'西', u'冬']),   # 东 -> deck 1, 西 -> deck R, 冬 -> deck R
            'new_hanzi': json.dumps([u'李', u'南'])        # 南 -> deck C, new Hanzi, 李 -> deck C
        }

        response = self.client.post(url, data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, 2)
        self.assertEqual(Hanzi.objects.all().count(), 9)  # including 王 added during Setup
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'东')).leitner_deck, '1')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'西')).leitner_deck, 'R')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'李')).leitner_deck, 'C')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'南')).leitner_deck, 'C')
        for h in retired_hanzis:
            self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=h)).leitner_deck, 'R')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'南')).forget_count, 1)
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'东')).repeat_count, 1)
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'西')).repeat_count, 1)
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'李')).repeat_count, 0)  # 北 is new
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'南')).repeat_count, 1)

    def test_set_leitner_record_existing_hanzi_stay_in_deck_C(self):
        # arrange
        _create_one_leitner_record(self.user, self.category.name, u'东', 'C')
        _create_one_leitner_record(self.user, self.category.name, u'北', 'C')
        count = 12
        _create_one_HanziStudyCount_instance(self.user, self.category, count)  # irrelate setting

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        data = {
            'category': self.category.name,
            'grasped_hanzi': json.dumps([]),
            'new_hanzi': json.dumps([u'东'])  # 东 stay deck C
        }

        response = self.client.post(url, data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count+1)
        self.assertEqual(Hanzi.objects.all().count(), 3)  # including 王 added during Setup
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'东')).leitner_deck, 'C')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'北')).leitner_deck, 'C')

    def test_set_leitner_record_existing_hanzi_move_to_deck_C_from_progressing_deck(self):
        # arrange
        _create_one_leitner_record(self.user, self.category.name, u'东', '2')
        _create_one_leitner_record(self.user, self.category.name, u'北', 'C')
        count = 12
        _create_one_HanziStudyCount_instance(self.user, self.category, count)  # irrelate setting

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        data = {
            'category': self.category.name,
            'grasped_hanzi': json.dumps([]),
            'new_hanzi': json.dumps([u'东'])  # 东 stay deck C
        }

        response = self.client.post(url, data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count+1)
        self.assertEqual(Hanzi.objects.all().count(), 3)  # including 王 added during Setup
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'东')).leitner_deck, 'C')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'北')).leitner_deck, 'C')

    def test_set_leitner_record_existing_hanzi_move_to_deck_C_from_deck_R(self):
        # arrange
        _create_one_leitner_record(self.user, self.category.name, u'东', 'R')
        _create_one_leitner_record(self.user, self.category.name, u'北', 'C')
        count = 12
        _create_one_HanziStudyCount_instance(self.user, self.category, count)  # irrelate setting

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        data = {
            'category': self.category.name,
            'grasped_hanzi': json.dumps([]),
            'new_hanzi': json.dumps([u'东'])  # 东 stay deck C
        }

        response = self.client.post(url, data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count+1)
        self.assertEqual(Hanzi.objects.all().count(), 3)  # including 王 added during Setup
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'东')).leitner_deck, 'C')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'北')).leitner_deck, 'C')

    def test_set_leitner_record_add_new_hanzi_to_deck_C(self):
        # arrange
        _create_one_leitner_record(self.user, self.category.name, u'东', 'C')
        _create_one_leitner_record(self.user, self.category.name, u'北', 'C')
        count = 12
        _create_one_HanziStudyCount_instance(self.user, self.category, count)  # irrelate setting

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        data = {
            'category': self.category.name,
            'grasped_hanzi': json.dumps([u'东']),   # 东 stay -> deck 2, as current count is 12
            'new_hanzi': json.dumps([])
        }

        response = self.client.post(url, data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count+1)
        self.assertEqual(Hanzi.objects.all().count(), 3)  # including 王 added during Setup
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'东')).leitner_deck, '2')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'北')).leitner_deck, 'C')

    def test_set_leitner_record_existing_hanzi_move_from_deck_C_to_progress_deck(self):
        # arrange
        _create_one_leitner_record(self.user, self.category.name, u'北', 'C')
        count = 12
        _create_one_HanziStudyCount_instance(self.user, self.category, count)  # irrelate setting

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        data = {
            'category': self.category.name,
            'grasped_hanzi': json.dumps([]),
            'new_hanzi': json.dumps([u'东'])  # 东 stay deck C
        }

        response = self.client.post(url, data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count+1)
        self.assertEqual(Hanzi.objects.all().count(), 3)  # including 王 added during Setup
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'东')).leitner_deck, 'C')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'北')).leitner_deck, 'C')

    def test_set_leitner_record_move_to_deck_R(self):
        # arrange
        _create_one_leitner_record(self.user, self.category.name, u'东', '3')
        _create_one_leitner_record(self.user, self.category.name, u'北', 'R')
        count = 12
        _create_one_HanziStudyCount_instance(self.user, self.category, count)   # 2 is the last number in deck '3'

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        data = {
            'category': self.category.name,
            'grasped_hanzi': json.dumps([u'东']),     # 东 -> deck R
            'new_hanzi': json.dumps([])
        }

        response = self.client.post(url, data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count+1)
        self.assertEqual(Hanzi.objects.all().count(), 3)  # including 王 added during Setup
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'东')).leitner_deck, 'R')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'北')).leitner_deck, 'R')
