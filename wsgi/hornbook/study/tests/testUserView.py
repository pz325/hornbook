# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

import util


class UserViewTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = util.create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)
        self.card = util.create_one_Card_instance()
        self.category = util.create_one_Category_instance(self.user, self.card.id, 'category')

        another_user = util.create_one_User_instance('another_user')
        another_category = util.create_one_Category_instance(another_user, self.card.id, 'another_category')
        util.create_one_HanziStudyCount_instance(another_user, another_category, 10)

        hanzi = u'王'
        category = util.create_one_Category_instance(another_user, self.card.id, 'category_for_another_user')
        util.create_one_HanziStudyRecord_instance(another_user, category, hanzi)

    def test_list_User(self):
        # arrange
        count = 3
        util.create_one_HanziStudyCount_instance(self.user, self.category, count)
        hanzi = u'风'
        util.create_one_HanziStudyRecord_instance(self.user, self.category, hanzi)

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
        util.create_one_HanziStudyCount_instance(self.user, self.category, count)
        hanzi = u'风'
        util.create_one_HanziStudyRecord_instance(self.user, self.category, hanzi)

        # act
        url = reverse('user-detail', args=[1])
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['study_records']), 1)
        self.assertEqual(response.data['study_records'][0], 'http://testserver' + reverse('hanzistudyrecord-detail', args=[2]))
