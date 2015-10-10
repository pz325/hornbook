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


def _create_one_HanziStudyCount_instance(user, count):
    HanziStudyCount.objects.create(
        user=user,
        count=count
        )


def _create_one_User_instance(username):
    User.objects.create(username=username)
    return User.objects.get(username=username)


def _create_one_HanziStudyRecord_instance(user, hanzi):
    hanzi_instance, _ = Hanzi.objects.get_or_create(content=hanzi)
    HanziStudyRecord.objects.create(
        user=user,
        hanzi=hanzi_instance
        )


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
    def function():
        pass
