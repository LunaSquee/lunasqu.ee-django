from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='forum-index'),
    url(r'^(\d+)/$', views.forum, name='forum-detail'),
    url(r'^topic/(\d+)/$', views.topic, name='topic-detail'),
    url(r'^reply/(\d+)/$', views.post_reply, name='reply'),
    url(r'newtopic/(\d+)/$', views.new_topic, name='new-topic'),
]