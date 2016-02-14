from django.test import TestCase

from study.models.leitner import is_last_number_on_deck
from study.models.leitner import to_review
from study.models.leitner import decks_to_review


class LeitnerTests(TestCase):
    def test_is_last_number_on_deck(self):
        self.assertTrue(is_last_number_on_deck('0', 9))
        self.assertTrue(is_last_number_on_deck('1', 0))
        self.assertTrue(is_last_number_on_deck('3', 12))
        self.assertFalse(is_last_number_on_deck('2', 0))

    def test_to_review(self):
        self.assertTrue(to_review('0', 12))
        self.assertTrue(to_review('0', 5))
        self.assertTrue(to_review('0', 20))

    def test_decks_to_review(self):
        decks_ids = decks_to_review(12)
        self.assertListEqual(['0', '2', '3', '7'], decks_ids)
