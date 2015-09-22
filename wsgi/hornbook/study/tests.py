from django.test import TestCase


class StudyTestCase(TestCase):
    def setUp(self):
        pass

    def test_dummy(self):
        '''dummy test'''
        self.assertEqual(True, True)


from leitner import get_deck_id


class LeitnerTestCase(TestCase):
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
