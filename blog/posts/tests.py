from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Post
from .utils import count_words, calculate_read_time


class UtilsTests(TestCase):
    def test_word_count(self):
        html = "<h1>This is no a pipe</h1>"
        count = count_words(html)
        self.assertEquals(5, count)

    def test_calculate_read_time(self):
        self.assertEqual(5, calculate_read_time(1000))


def create_post(title, slug, content, publish=None):
    """
    Creates a post with the given title, slug, content,
    and publish date.
    """
    if publish is None:
        publish = timezone.now()

    return Post.objects.create(title=title,
                               slug=slug,
                               content=content,
                               publish=publish)


class PostViewTests(TestCase):
    def test_list_view_with_no_posts(self):
        """
        Test the list page has loaded correctly with no posts
        """
        response = self.client.get(reverse('posts:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post List')
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_list_view_with_a_single_post(self):
        """
        Test the list page with a single post
        """
        create_post(title='First Post', slug='first-post',
                    content='This is some simple text.')
        response = self.client.get(reverse('posts:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First Post')
        self.assertQuerysetEqual(response.context['posts'], ['<Post: First Post>'])
