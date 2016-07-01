from django.template import RequestContext

from django.forms import models as forms_models

from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response, get_object_or_404, render

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.template.context_processors import csrf

from forum.models import Section, Forum, Topic, Post
from forum.forms import TopicForm, PostForm

from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

from forum.settings import *

from personal.bleach import bleach_clean

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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

@permission_required("forum.can_pin_topic")
def pintopic(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    
    if topic.pinned:
        topic.pinned = False
    else:
        topic.pinned = True
    topic.save()

    return HttpResponseRedirect(reverse('forum-detail', args=(topic.forum.id, )))

@permission_required("forum.can_close_topic")
def closetopic(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    
    if topic.closed:
        topic.closed = False
    else:
        topic.closed = True
    topic.save()

    return HttpResponseRedirect(reverse('forum-detail', args=(topic.forum.id, )))

@permission_required("forum.can_lock_forum")
def closeforum(request, forum_id):
    forum = Forum.objects.get(pk=forum_id)
    
    if forum.closed:
        forum.closed = False
    else:
        forum.closed = True
    forum.save()

    return HttpResponseRedirect(reverse('forum-index'))

def forum(request, forum_id, slug):
    """Listing of topics in a forum."""
    topics = Topic.objects.filter(forum=forum_id).order_by("-pinned", "-created")
    topics = mk_paginator(request, topics, DJANGO_SIMPLE_FORUM_TOPICS_PER_PAGE)

    forum = get_object_or_404(Forum, pk=forum_id)

    return render_to_response("forum/forum.html", add_csrf(request, topics=topics, pk=forum_id, forum=forum, section=forum.section),
                              context_instance=RequestContext(request))

def section(request, slug):
    section = Section.objects.get(slug=slug)
    
    if not section:
        return render(request, 'personal/basic.html', {'content':['No such forum section.']})

    forums = Forum.objects.filter(section=section)

    return render_to_response("forum/section.html", add_csrf(request, forums=forums, section=section),
                              context_instance=RequestContext(request))

def topic(request, topic_id, slug):
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
    user = request.user

    if topic.closed:
        return render(request, 'personal/basic.html', {'content':['This topic is closed.']})

    if topic.forum.closed and not user.has_perm('forum.can_post_lock_forum'):
        return render(request, 'personal/basic.html', {'content':['This forum is locked.']})

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():

            post = Post()
            post.topic = topic
            post.title = 'RE: '+topic.title
            post.body = bleach_clean(form.cleaned_data['body'])
            post.creator = request.user
            post.user_ip = get_client_ip(request)

            post.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(topic.id, topic.slug, )))

    return render_to_response('forum/reply.html', {
            'form': form,
            'topic': topic,
            'forum': topic.forum,
            'editing': False,
        }, context_instance=RequestContext(request))

@login_required
def post_reply_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    topic = post.topic
    user = request.user
    form = PostForm(instance=post)

    if not user.id == post.creator.id:
         return render(request, 'personal/basic.html', {'content':['You do not own this post.']})
    
    if topic.closed:
        return render(request, 'personal/basic.html', {'content':['This topic is closed.']})

    if topic.forum.closed and not user.has_perm('forum.can_post_lock_forum'):
        return render(request, 'personal/basic.html', {'content':['This forum is locked.']})

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():

            post.body = bleach_clean(form.cleaned_data['body'])
            post.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(topic.id, topic.slug, )))

    return render_to_response('forum/reply.html', {
            'form': form,
            'topic': topic,
            'forum': topic.forum,
            'editing': True,
        }, context_instance=RequestContext(request))

@login_required
def new_topic(request, forum_id):
    form = TopicForm()
    forum = get_object_or_404(Forum, pk=forum_id)
    user = request.user
    
    if forum.closed and not user.has_perm('forum.can_post_lock_forum'):
        return render(request, 'personal/basic.html', {'content':['This forum is locked.']})

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():

            topic = Topic()
            topic.title = form.cleaned_data['title']
            topic.description = bleach_clean(form.cleaned_data['description'])
            topic.forum = forum
            topic.creator = user

            topic.save()

            tpkPost = Post()
            tpkPost.topic = topic
            tpkPost.title = topic.title
            tpkPost.body = bleach_clean(form.cleaned_data['description'])
            tpkPost.creator = user
            tpkPost.user_ip = get_client_ip(request)

            tpkPost.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(topic.id, topic.slug, )))

    return render_to_response('forum/new-topic.html', {
            'form': form,
            'forum': forum,
        }, context_instance=RequestContext(request))
