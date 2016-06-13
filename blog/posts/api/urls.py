from django.conf.urls import url

from .views import (PostListAPIView,
                    PostRetrieveAPIView,
                    PostUpdateAPIView,
                    PostDestroyAPIView,
                    PostCreateAPIView)

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^create$', PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', PostRetrieveAPIView.as_view(), name='detail'),
    url(r'^edit/(?P<pk>\d+)/$', PostUpdateAPIView.as_view(), name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', PostDestroyAPIView.as_view(), name='delete'),
]
