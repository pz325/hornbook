from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from study.models.category import Category

from random import randint
import util


class CategoryViewTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = util.create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)
        self.card = util.create_one_Card_instance()

    def test_create(self):
        # arrange
        url = reverse('category-list')
        display = 'mydisplay'
        num_retired = 15

        data = {
            'display': display,
            'num_retired': num_retired,
            'card_id': self.card.id
        }

        # act
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Category.objects.get(user=self.user).display, display)
        self.assertEqual(Category.objects.get(user=self.user).num_retired, num_retired)

    def test_create_without_display(self):
        # arrange
        url = reverse('category-list')
        default_display = 'display'
        num_retired = 15

        data = {
            'num_retired': num_retired,
            'card_id': self.card.id
        }

        # act
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Category.objects.get(user=self.user).display, default_display)
        self.assertEqual(Category.objects.get(user=self.user).num_retired, num_retired)

    def test_create_without_num_retired(self):
        # arrange
        url = reverse('category-list')
        display = 'mydisplay'
        default_num_retired = 10
        data = {
            'display': display,
            'card_id': self.card.id
        }

        # act
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Category.objects.get(user=self.user).display, display)
        self.assertEqual(Category.objects.get(user=self.user).num_retired, default_num_retired)

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
        index = randint(0, num_to_create)

        # act
        url = reverse('category-detail', args=[index+1])  # index is 0 based, but API pk is 1 based
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['display'], displays[index])

    def test_put_one(self):
        # arrange
        num_to_create = randint(20, 40)
        util.create_Category_instances(self.user, num_to_create)
        index = randint(0, num_to_create)

        # act
        new_display = 'new_display'
        new_num_retired = 35
        data = {
            'display': new_display,
            'num_retired': new_num_retired,
            'card_id': self.card.id
        }
        url = reverse('category-detail', args=[index+1])  # index is 0 based, but API pk is 1 based
        response = self.client.put(url, data=data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.filter(user=self.user).count(), num_to_create)
        self.assertEqual(Category.objects.filter(user=self.user)[index].display, new_display)
        self.assertEqual(Category.objects.filter(user=self.user)[index].num_retired, new_num_retired)

    def test_delete_one(self):
        # arrange
        num_to_create = randint(20, 40)
        util.create_Category_instances(self.user, num_to_create)
        index = randint(0, num_to_create-1)

        # act
        url = reverse('category-detail', args=[index+1])
        response = self.client.delete(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.filter(user=self.user).count(), num_to_create-1)
