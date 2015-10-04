from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from study.models import HanziStudyCount
from django.contrib.auth.models import User


class StudyTestCase(TestCase):
    def setUp(self):
        pass

    def test_dummy(self):
        '''dummy test'''
        self.assertEqual(True, True)


from leitner import get_deck_id


class LeitnerTests(TestCase):
    def test_get_correct_level1_cards(self):
        session_counts = range(0, 10)
        expected_deck_ids = range(0, 10)
        for session_count, expected_deck_id in zip(session_counts, expected_deck_ids):
            deck_id = get_deck_id(session_count=session_count, level=1)
            self.assertEqual(expected_deck_id, deck_id)

    def test_get_correct_level2_cards(self):
        session_counts = range(0, 10)
        expected_deck_ids = (8, 9, 0, 1, 2, 3, 4, 5, 6, 7)
        for session_count, expected_deck_id in zip(session_counts, expected_deck_ids):
            deck_id = get_deck_id(session_count=session_count, level=2)
            self.assertEqual(expected_deck_id, deck_id)

    def test_get_correct_level3_cards(self):
        session_counts = range(0, 10)
        expected_deck_ids = (5, 6, 7, 8, 9, 0, 1, 2, 3, 4)
        for session_count, expected_deck_id in zip(session_counts, expected_deck_ids):
            deck_id = get_deck_id(session_count=session_count, level=3)
            self.assertEqual(expected_deck_id, deck_id)

    def test_get_correct_level4_cards(self):
        session_counts = range(0, 10)
        expected_deck_ids = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
        for session_count, expected_deck_id in zip(session_counts, expected_deck_ids):
            deck_id = get_deck_id(session_count=session_count, level=4)
            self.assertEqual(expected_deck_id, deck_id)


class HanziStudyCountTests(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        User.objects.create(username=self.username)
        self.user = User.objects.get(username=self.username)
        self.client.force_authenticate(user=self.user)

    def _create_one_HanziStudyCount_instance(self, count):
        url = reverse('hanzistudycount-list')
        data = {'count': count}
        self.client.post(url, data, format='json')

    def test_create_HanziStudyCount(self):
        # arrange
        url = reverse('hanzistudycount-list')
        count = 3
        data = {'count': count}

        # act
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HanziStudyCount.objects.count(), 1)
        self.assertEqual(HanziStudyCount.objects.get().count, count)
        self.assertEqual(HanziStudyCount.objects.get().user.username, self.username)

    def test_list_HanziStudyCount(self):
        # arrange
        count = 3
        self._create_one_HanziStudyCount_instance(count)

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
        self._create_one_HanziStudyCount_instance(count)

        # act
        url = reverse('hanzistudycount-detail', args=[self.user.id])
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], count)

    def test_put_one_HanziStudyCount(self):
        # arrange
        count = 3
        self._create_one_HanziStudyCount_instance(count)

        # act
        count = 6
        data = {'count': count}
        url = reverse('hanzistudycount-detail', args=[self.user.id])
        put_response = self.client.put(url, data=data, format='json')
        get_response = self.client.get(url)

        # assert
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['count'], count)

    def test_delete_one_HanziStudyCount(self):
        # arrange
        count = 3
        self._create_one_HanziStudyCount_instance(count)

        # act
        url = reverse('hanzistudycount-detail', args=[self.user.id])
        delete_response = self.client.delete(url)
        get_response = self.client.get(url)

        # assert
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
