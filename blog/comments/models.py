from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CommentManager(models.Manager):
    def all(self):
        """
        Return all comments (not replies).
        Note, replies are comments with a parent value.
        """
        return super().filter(parent=None)

    def filter_by_instance(self, instance=None):
        """Retrieve the comments (not replies) for the given post"""
        content_type = ContentType.objects.get_for_model(instance.__class__)

        return super().filter(content_type=content_type, object_id=instance.id).filter(parent=None)

    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            some_model = model_qs.first().model_class()
            obj_qs = some_model.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self', null=True, blank=True)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.user.username)

    def children(self):  # replies
        return Comment.objects.filter(parent=self)

    @property
    def absolute_url(self):
        return reverse('comments:thread', args=(self.id,))

    @property
    def delete_url(self):
        return reverse('comments:delete', args=(self.id,))

    @property
    def is_parent(self):
        return self.parent is None
