import datetime
from math import ceil
import re

from django.utils.html import strip_tags


def count_words(html):
    return len(re.findall(r'\w+', strip_tags(html)))


def calculate_read_time(word_count, word_per_minute=200):
    read_time = ceil(word_count / word_per_minute)
    return str(datetime.timedelta(minutes=read_time))


def get_read_time(html):
    return calculate_read_time(count_words(html))

