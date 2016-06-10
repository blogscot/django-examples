from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='list'),
    url(r'^create$', views.post_create, name='create'),
    url(r'^(?P<slug>\w+)/$', views.post_detail, name='detail'),
    url(r'^edit/(?P<slug>\w+)/$', views.post_edit, name='edit'),
    url(r'^delete/(?P<slug>\w+)/$', views.post_delete, name='delete'),
]
