from django.views.generic import TemplateView
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="personal/index.html", content_type="text/html"), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name="personal/about.html", content_type="text/html"), name='about'),
    url(r'^chat/$', TemplateView.as_view(template_name="personal/chat.html", content_type="text/html"), name='chat'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
