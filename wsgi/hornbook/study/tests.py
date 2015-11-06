# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from study.models import HanziStudyCount
from study.models import HanziStudyRecord
from lexicon.models import Hanzi
from django.contrib.auth.models import User

from leitner import is_last_number_on_deck
from leitner import to_review
from leitner import decks_to_review

import json


def _create_one_HanziStudyCount_instance(user, count):
    return HanziStudyCount.objects.create(
        user=user,
        count=count
        )


def _create_one_User_instance(username):
    return User.objects.create(username=username)


def _create_one_HanziStudyRecord_instance(user, hanzi):
    hanzi_instance, _ = Hanzi.objects.get_or_create(content=hanzi)
    return HanziStudyRecord.objects.create(
        user=user,
        hanzi=hanzi_instance
        )


def _create_one_leitner_record(user, hanzi, deck_id):
    hanzi_instance, _ = Hanzi.objects.get_or_create(content=hanzi)
    return HanziStudyRecord.objects.create(
        user=user,
        hanzi=hanzi_instance,
        leitner_deck=deck_id)


class LeitnerTests(TestCase):
    def test_is_last_number_on_deck(self):
        self.assertTrue(is_last_number_on_deck('0', 9))
        self.assertTrue(is_last_number_on_deck('1', 0))
        self.assertFalse(is_last_number_on_deck('2', 0))

    def test_to_review(self):
        self.assertTrue(to_review('0', 12))
        self.assertTrue(to_review('0', 5))
        self.assertTrue(to_review('0', 20))

    def test_decks_to_review(self):
        decks_ids = decks_to_review(12)
        self.assertListEqual(['0', '2', '3', '7'], decks_ids)


class HanziStudyCountViewSetTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = _create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)

        another_user = _create_one_User_instance('another_user')
        _create_one_HanziStudyCount_instance(another_user, 10)

    def test_create_HanziStudyCount(self):
        # arrange
        url = reverse('hanzistudycount-list')
        count = 3
        data = {'count': count}

        # act
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HanziStudyCount.objects.filter(user=self.user).count(), 1)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count)

    def test_list_HanziStudyCount(self):
        # arrange
        count = 3
        _create_one_HanziStudyCount_instance(self.user, count)

        # act
        url = reverse('hanzistudycount-list')
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['count'], count)

    def test_get_one_HanziStudyCount(self):
        # arrange
        count = 3
        _create_one_HanziStudyCount_instance(self.user, count)

        # act
        url = reverse('hanzistudycount-detail', args=[self.user.id])
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], count)

    def test_put_one_HanziStudyCount(self):
        # arrange
        count = 3
        _create_one_HanziStudyCount_instance(self.user, count)

        # act
        count = 6
        data = {'count': count}
        url = reverse('hanzistudycount-detail', args=[self.user.id])
        response = self.client.put(url, data=data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.filter(user=self.user).count(), 1)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count)

    def test_delete_one_HanziStudyCount(self):
        # arrange
        count = 3
        _create_one_HanziStudyCount_instance(self.user, count)

        # act
        url = reverse('hanzistudycount-detail', args=[self.user.id])
        response = self.client.delete(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HanziStudyCount.objects.filter(user=self.user).count(), 0)


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = _create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)

        another_user = _create_one_User_instance('another_user')
        _create_one_HanziStudyCount_instance(another_user, 10)
        hanzi = u'王'
        _create_one_HanziStudyRecord_instance(another_user, hanzi)

    def test_list_User(self):
        # arrange
        count = 3
        _create_one_HanziStudyCount_instance(self.user, count)
        hanzi = u'风'
        _create_one_HanziStudyRecord_instance(self.user, hanzi)

        # act
        url = reverse('user-list')
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result_data = response.data['results']
        self.assertEqual(len(result_data), 1)
        self.assertEqual(result_data[0]['username'], self.user.username)
        self.assertEqual(result_data[0]['study_counts'], count)
        self.assertEqual(len(result_data[0]['study_records']), 1)
        self.assertEqual(result_data[0]['study_records'][0], 'http://testserver' + reverse('hanzistudyrecord-detail', args=[2]))

    def test_get_one_User(self):
        # arrange
        count = 3
        _create_one_HanziStudyCount_instance(self.user, count)
        hanzi = u'风'
        _create_one_HanziStudyRecord_instance(self.user, hanzi)

        # act
        url = reverse('user-detail', args=[1])
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['study_counts'], count)
        self.assertEqual(len(response.data['study_records']), 1)
        self.assertEqual(response.data['study_records'][0], 'http://testserver' + reverse('hanzistudyrecord-detail', args=[2]))


class HanziStudyRecordViewSetTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = _create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)

        another_user = _create_one_User_instance('another_user')
        _create_one_HanziStudyRecord_instance(another_user, u'王')

    def test_list_HanziStudyRecord(self):
        # arrange
        hanzis = [u'东', u'南']
        for h in hanzis:
            _create_one_HanziStudyRecord_instance(self.user, h)

        # act
        url = reverse('hanzistudyrecord-list')
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_HanziStudyRecord(self):
        # arrange
        url = reverse('hanzistudyrecord-list')
        hanzi = u'东'
        data = {'hanzi': hanzi}

        # act
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HanziStudyRecord.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Hanzi.objects.filter(content=hanzi).count(), 1)
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user).hanzi, Hanzi.objects.get(content=hanzi))

    def test_get_one_HanziStudyRecord(self):
        # arrange
        hanzi = u'东'
        hanzi_study_record_instance = _create_one_HanziStudyRecord_instance(self.user, hanzi)

        # act
        url = reverse('hanzistudyrecord-detail', args=[hanzi_study_record_instance.id])
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['hanzi'], hanzi)

    def test_put_one_HanziStudyRecord(self):
        # arrange
        hanzi = u'东'
        hanzi_study_record_instance = _create_one_HanziStudyRecord_instance(self.user, hanzi)

        # act
        hanzi = u'王'
        data = {'hanzi': hanzi}
        url = reverse('hanzistudyrecord-detail', args=[hanzi_study_record_instance.id])
        response = self.client.put(url, data=data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyRecord.objects.filter(user=self.user).count(), 1)
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user), hanzi_study_record_instance)

    def test_delete_one_HanziStudyRecord(self):
        # arrange
        hanzi = u'东'
        hanzi_study_record_instance = _create_one_HanziStudyRecord_instance(self.user, hanzi)

        # act
        url = reverse('hanzistudyrecord-detail', args=[hanzi_study_record_instance.id])
        response = self.client.delete(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HanziStudyRecord.objects.filter(user=self.user).count(), 0)

    def test_get_leitner_record(self):
        # arrange
        current_deck_instance = _create_one_leitner_record(self.user, u'东', 'C')
        progress_1_deck_instance = _create_one_leitner_record(self.user, u'南', '1')
        progress_2_deck_instance = _create_one_leitner_record(self.user, u'西', '3')
        _create_one_HanziStudyCount_instance(self.user, 1)

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_leitner_record_with_num_retired(self):
        # arrange
        retired_hanzis = [u'北', u'春', u'夏', u'冬']
        _create_one_leitner_record(self.user, u'东', 'C')
        _create_one_leitner_record(self.user, u'南', '1')
        _create_one_leitner_record(self.user, u'西', '3')
        for h in retired_hanzis:
            _create_one_leitner_record(self.user, h, 'R')
        _create_one_HanziStudyCount_instance(self.user, 1)

        # act
        num_retired = 2
        url = reverse('hanzistudyrecord-list') + '/leitner_record?num_retired={num_retired}'.format(num_retired=num_retired)
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # two from deck R
        for resp_data in response.data:
            if resp_data['hanzi'] in retired_hanzis:
                self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=resp_data['hanzi'])).repeat_count, 1)

    def test_set_leitner_record(self):
        # arrange
        current_deck_instance = _create_one_leitner_record(self.user, u'东', 'C')
        progress_1_deck_instance = _create_one_leitner_record(self.user, u'南', '1')
        progress_2_deck_instance = _create_one_leitner_record(self.user, u'西', '2')
        _create_one_HanziStudyCount_instance(self.user, 1)

        # act
        url = reverse('hanzistudyrecord-list') + '/leitner_record'
        data = {
            'grasped_hanzi': json.dumps([u'东', u'西']),   # 东 -> deck 1, 西 -> deck R
            'new_hanzi': json.dumps([u'北', u'南'])        # 北 -> deck C, new Hanzi, 南 -> deck C
        }

        response = self.client.post(url, data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, 2)
        self.assertEqual(Hanzi.objects.all().count(), 5)  # including 王 added during Setup
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'东')).leitner_deck, '1')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'西')).leitner_deck, 'R')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'北')).leitner_deck, 'C')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'南')).leitner_deck, 'C')
        self.assertEqual(HanziStudyRecord.objects.get(user=self.user, hanzi=Hanzi.objects.get(content=u'南')).forget_count, 1)
