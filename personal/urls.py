from django.views.generic import TemplateView
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
