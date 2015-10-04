# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from lexicon.models import Hanzi
from django.contrib.auth.models import User


def _create_one_User_instance(username):
    User.objects.create(username=username)


def _create_one_Hanzi_instance(hanzi):
    Hanzi.objects.create(content=hanzi)


class HanziViewSetTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        _create_one_User_instance(self.username)
        self.user = User.objects.get(username=self.username)
        self.client.force_authenticate(user=self.user)

    def test_list_Hanzi(self):
        # arrange
        hanzi1 = u'东'
        hanzi2 = u'西'
        _create_one_Hanzi_instance(hanzi1)
        _create_one_Hanzi_instance(hanzi2)

        # act
        url = reverse('hanzi-list')
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result_data = response.data['results']
        self.assertEqual(len(result_data), 2)
        hanzis = [result['content'] for result in result_data]
        self.assertIn(hanzi1, hanzis)
        self.assertIn(hanzi2, hanzis)

    def test_create_Hanzi(self):
        # act
        hanzi = u'东'
        url = reverse('hanzi-list')
        data = {'content': hanzi}
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hanzi.objects.count(), 1)
        self.assertEqual(Hanzi.objects.get().content, hanzi)

    def test_get_one_Hanzi_instance(self):
        # arrange
        hanzi = u'东'
        _create_one_Hanzi_instance(hanzi)

        # act
        url = reverse('hanzi-detail', args=[hanzi])
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], hanzi)

    def test_delete_one_Hanzi_instance(self):
        # arrange
        hanzi = u'东'
        _create_one_Hanzi_instance(hanzi)

        # act
        url = reverse('hanzi-detail', args=[hanzi])
        response = self.client.delete(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Hanzi.objects.count(), 0)
