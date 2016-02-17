from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from study.models.study import HanziStudyCount
import util


class HanziStudyCountViewTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.user = util.create_one_User_instance(self.username)
        self.client.force_authenticate(user=self.user)

        self.card = util.create_one_Card_instance()
        self.category = util.create_one_Category_instance(self.user, self.card.id, 'category')

        another_user = util.create_one_User_instance('another_user')
        another_category = util.create_one_Category_instance(another_user, self.card.id, 'another_category')
        util.create_one_HanziStudyCount_instance(another_user, another_category, 10)

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
        data = {'count': count, 'category_id': self.category.id}

        # act
        url = reverse('hanzistudycount-list')
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HanziStudyCount.objects.filter(user=self.user).count(), 1)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).category.id, self.category.id)

    def test_list_without_category_parameter(self):
        # arrange
        count = 3
        categoryA = util.create_one_Category_instance(self.user, self.card.id, 'categoryA')
        categoryB = util.create_one_Category_instance(self.user, self.card.id, 'categoryB')

        util.create_one_HanziStudyCount_instance(self.user, categoryA, count)
        util.create_one_HanziStudyCount_instance(self.user, categoryB, count)

        # act
        url = reverse('hanzistudycount-list')
        response = self.client.get(url, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list(self):
        # arrange
        count = 3
        util.create_one_HanziStudyCount_instance(self.user, self.category, count)

        # act
        url = reverse('hanzistudycount-list')
        url += '?category_id={category_id}'.format(category_id=self.category.id)
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
        study_count = util.create_one_HanziStudyCount_instance(self.user, self.category, count)

        # act
        url = reverse('hanzistudycount-detail', args=[study_count.id])
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], count)
        self.assertEqual(response.data['category'], self.category.id)

    def test_put_one(self):
        '''
        pk -- HanziStudyCount id
        '''
        # arrange
        count = 3
        study_count = util.create_one_HanziStudyCount_instance(self.user, self.category, count)

        # act
        count = 6
        data = {'count': count}
        url = reverse('hanzistudycount-detail', args=[study_count.id])
        response = self.client.put(url, data=data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HanziStudyCount.objects.filter(user=self.user).count(), 1)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).count, count)
        self.assertEqual(HanziStudyCount.objects.get(user=self.user).category.id, self.category.id)

    def test_delete_one(self):
        '''
        pk -- HanziStudyCount id
        '''
        # arrange
        count = 3
        study_count = util.create_one_HanziStudyCount_instance(self.user, self.category, count)

        # act
        url = reverse('hanzistudycount-detail', args=[study_count.id])
        response = self.client.delete(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HanziStudyCount.objects.filter(user=self.user).count(), 0)
