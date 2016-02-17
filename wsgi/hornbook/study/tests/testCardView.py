from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from study.models.card import Card

from random import randint
import util


class CardViewTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = util.create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)

    def test_create(self):
        # arrange
        url = reverse('card-list')
        font_size = 'font_size'
        data = {
            'font_size': font_size
        }

        # act
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.all().count(), 1)
        self.assertEqual(Card.objects.all()[0].font_size, font_size)

    def test_list(self):
        # arrange
        font_size1 = 'font_size1'
        font_size2 = 'font_size2'
        util.create_one_Card_instance(font_size1)
        util.create_one_Card_instance(font_size2)

        # act
        url = reverse('card-list')
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['font_size'], font_size1)

    def test_get_one(self):
        # arrange
        num_to_create = randint(20, 40)
        font_sizes = util.create_Card_instances(num_to_create)
        index = randint(0, num_to_create-1)

        # act
        url = reverse('card-detail', args=[index+1])  # index is 0 based, but API pk is 1 based
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['font_size'], font_sizes[index])

    def test_put_one(self):
        # arrange
        num_to_create = randint(20, 40)
        util.create_Card_instances(num_to_create)
        index = randint(0, num_to_create-1)

        # act
        new_font_size = 'new_font_size'
        data = {
            'font_size': new_font_size
        }
        url = reverse('card-detail', args=[index+1])  # index is 0 based, but API pk is 1 based
        response = self.client.put(url, data=data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Card.objects.all().count(), num_to_create)
        self.assertEqual(Card.objects.all()[index].font_size, new_font_size)

    def test_delete_one(self):
        # arrange
        num_to_create = randint(20, 40)
        util.create_Card_instances(num_to_create)
        index = randint(0, num_to_create-1)

        # act
        url = reverse('card-detail', args=[index+1])
        response = self.client.delete(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Card.objects.all().count(), num_to_create-1)
