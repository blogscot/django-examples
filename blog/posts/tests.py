from datetime import timedelta

from django.test import TestCase

from .utils import count_words, calculate_read_time


class UtilsTests(TestCase):

    def test_word_count(self):
        html = "<h1>This is no a pipe</h1>"
        count = count_words(html)
        self.assertEquals(5, count)

    def test_calculate_read_time(self):
        self.assertEqual(5, calculate_read_time(1000))
