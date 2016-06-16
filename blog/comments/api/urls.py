from django.conf.urls import url

from .views import (
     CommentListAPIView,
     CommentCreateAPIView,
     CommentRetrieveAPIView,
     )

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', CommentRetrieveAPIView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/delete/$', CommentDeleteAPIView.as_view(), name='delete'),
]
