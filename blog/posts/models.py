from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown

from comments.models import Comment


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super().filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "{!s}/{!s}".format(instance.id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True, blank=True,
                              width_field='width_field',
                              height_field='height_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField('date published', auto_now=False, auto_now_add=True)

    objects = PostManager()  # filter hook

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated', '-timestamp']

    @property
    def markdown(self):
        return mark_safe(markdown(self.content))

    @property
    def comments(self):
        return Comment.objects.filter_by_instance(self)

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.__class__)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    posts = Post.objects.filter(slug=slug).order_by('-id')
    if posts.exists():
        new_slug = "{!s}-{!s}".format(slug, posts.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
