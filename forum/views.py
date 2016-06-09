from django.template import RequestContext

from django.forms import models as forms_models

from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response, get_object_or_404, render

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.template.context_processors import csrf

from forum.models import Section, Forum, Topic, Post
from forum.forms import TopicForm, PostForm

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from forum.settings import *

import bleach

bleach_tags = [
    'img', 'em', 'strong', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'br', 'a', 'embed', 'ul', 'li', 'ol', 'hr', 
    'i', 's', 'table', 'tbody', 'td', 'tr', 'blockquote', 'code', 'caption', 'big', 'small', 'q', 'div', 'cite'
]

bleach_attrs = {
    'div': ['style'],
    'span': ['class', 'style', 'dir'],
    'table': ['border', 'cellpadding', 'style', 'cellspacing'],
    'a': ['href', 'title', 'rel'],
    'img': ['alt', 'style', 'src'],
    'embed': ['type', 'class', 'src', 'width', 'height', 'allowfullscreen', 'loop', 'menu', 'play', 'src', 'style', 'wmode']
}

bleach_styles = [
    'font-size', 'color', 'font-weigth', 'float', 'text-align', 'background', 'font-family', 'border', 'padding'
]

def mk_user_meta(user):
    metadict = user

def index(request):
    """Main listing."""
    sections = Section.objects.all()
    forums = Forum.objects.all().order_by('id')
    
    forsect = {}
    for forum in forums:
        if forum.section.title in forsect:
            forsect[forum.section.title]['forums'].append(forum)
        else:
            forsect[forum.section.title] = {'forums': [forum], 'description': forum.section.description}

    return render_to_response("forum/list.html", {'sections': sections, 'forums': forums, 
                                'user': request.user,
                                'sectionlist': forsect}, 
                                context_instance=RequestContext(request))


def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def forum(request, forum_id):
    """Listing of topics in a forum."""
    topics = Topic.objects.filter(forum=forum_id).order_by("-pinned", "-created")
    topics = mk_paginator(request, topics, DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE)

    forum = get_object_or_404(Forum, pk=forum_id)

    return render_to_response("forum/forum.html", add_csrf(request, topics=topics, pk=forum_id, forum=forum, section=forum.section),
                              context_instance=RequestContext(request))

def topic(request, topic_id):
    """Listing of posts in a topic."""
    posts = Post.objects.filter(topic=topic_id).order_by("created")
    lessen_posts = mk_paginator(request, posts, DJANGO_SIMPLE_FORUM_REPLIES_PER_PAGE)
    topic = Topic.objects.get(pk=topic_id)
    return render_to_response("forum/topic.html", add_csrf(request, posts=lessen_posts, pk=topic_id,
        topic=topic, forum=topic.forum, section=topic.forum.section, post_count=len(posts)), context_instance=RequestContext(request))

@login_required
def post_reply(request, topic_id):
    form = PostForm()
    topic = Topic.objects.get(pk=topic_id)
    
    if topic.closed:
        return render(request, 'personal/basic.html', {'content':['This topic is closed.']})

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():

            post = Post()
            post.topic = topic
            post.title = 'RE: '+topic.title
            post.body = bleach.clean(form.cleaned_data['body'], tags=bleach_tags, attributes=bleach_attrs, styles=bleach_styles)
            post.creator = request.user
            post.user_ip = request.META['REMOTE_ADDR']

            post.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(topic.id, )))

    return render_to_response('forum/reply.html', {
            'form': form,
            'topic': topic,
            'forum': topic.forum,
        }, context_instance=RequestContext(request))

@login_required
def new_topic(request, forum_id):
    form = TopicForm()
    forum = get_object_or_404(Forum, pk=forum_id)
    
    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():

            topic = Topic()
            topic.title = form.cleaned_data['title']
            topic.description = bleach.clean(form.cleaned_data['description'], tags=bleach_tags, attributes=bleach_attrs, styles=bleach_styles)
            topic.forum = forum
            topic.creator = request.user

            topic.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(topic.id, )))

    return render_to_response('forum/new-topic.html', {
            'form': form,
            'forum': forum,
        }, context_instance=RequestContext(request))
