from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from random import randint
import util


class CategoryViewTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = util.create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)
        self.card = util.create_one_Card_instance()

    def test_list(self):
        # arrange
        display1 = 'mydisplay1'
        display2 = 'mydisplay2'
        util.create_one_Category_instance(user=self.user, card_id=self.card.id, display=display1)
        util.create_one_Category_instance(user=self.user, card_id=self.card.id, display=display2)

        # act
        url = reverse('category-list')
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['display'], display1)

    def test_get_one(self):
        # arrange
        num_to_create = randint(20, 40)
        displays = util.create_Category_instances(self.user, num_to_create)
        index = randint(0, num_to_create-1)

        # act
        url = reverse('category-detail', args=[index+1])  # index is 0 based, but API pk is 1 based
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['display'], displays[index])
