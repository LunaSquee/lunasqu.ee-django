from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from blog.models import Post
from .views import NewPostView, PostList

urlpatterns = [
	url(r'^$', PostList),
	url(r'^(?P<pk>\d+)(?:-(?P<slug>[\w\d-]+))?/$', DetailView.as_view(model=Post, template_name="blog/post.html"), name="view_blog_post"),
	url(r'^new_post/', NewPostView, name="new_post")
]
