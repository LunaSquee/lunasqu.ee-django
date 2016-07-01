from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.context_processors import csrf
from .forms import NewPostForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

from .models import Post

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

def PostList(request):
    posts = Post.objects.all().order_by("-created")
    
    posts = mk_paginator(request, posts, 20)

    return render_to_response("blog/blog.html", add_csrf(request, posts=posts), context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def NewPostView(request):
    if request.POST:
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/blog')

    else:
        form = NewPostForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form 

    return render_to_response('blog/new_entry.html', args, context_instance=RequestContext(request))
