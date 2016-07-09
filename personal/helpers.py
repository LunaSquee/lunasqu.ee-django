from django.core.paginator import Paginator
from django.template.context_processors import csrf

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

def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d
