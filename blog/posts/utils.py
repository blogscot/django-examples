import datetime
from math import ceil
import re

from django.utils.html import strip_tags


def count_words(html):
    return len(re.findall(r'\w+', strip_tags(html)))


def calculate_read_time(word_count, word_per_minute=200):
    return ceil(word_count / word_per_minute)


def get_read_time(html):
    return calculate_read_time(count_words(html))

