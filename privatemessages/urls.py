from django.views.generic import TemplateView
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.inbox, name='inbox'),
    url(r'^(?P<message_id>\d+)(?:/(?P<slug>[\w\d-]+))?/$', views.view, name='view_message'),
    url(r'^sent/$', views.outbox, name='outbox'),
    url(r'^compose(?:/(?P<recipient>[\w\d@\.+-_]+))?/$', views.compose, name='compose_message'),
    url(r'^reply/(?P<message_id>\d+)/$', views.reply, name='compose_message_reply'),
    url(r'^markread/(?P<message_id>\d+)/$', views.mark_read, name='message_mark_read'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^archive/(?P<message_id>\d+)/$', views.delete, name='message_delete'),
    url(r'^archive/restore/(?P<message_id>\d+)/$', views.undelete, name='message_undelete'),
]
