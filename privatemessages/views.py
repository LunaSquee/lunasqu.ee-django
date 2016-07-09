from django.shortcuts import render
from .models import PrivateMessage
from .forms import PrivateMessageComposeForm
from personal.helpers import mk_paginator, add_csrf
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.utils import timezone

@login_required
def compose(request, recipient=None):
    form = None

    if request.method == 'POST':
        form = PrivateMessageComposeForm(request.POST)
        if form.is_valid():
            form.save(sender=request.user)
            messages.success(request, 'Private message has been sent.')
            return HttpResponseRedirect(reverse('inbox'))

    else:
        form = PrivateMessageComposeForm()
        if recipient is not None:
            form.fields['recipient'].initial = recipient

    return render_to_response('pms/compose_message.html', {
            'form': form,
        }, context_instance=RequestContext(request))

@login_required
def reply(request, message_id):
    form = None

    parent = get_object_or_404(PrivateMessage, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == 'POST':
        form = PrivateMessageComposeForm(request.POST)
        if form.is_valid():
            form.save(sender=request.user, parent=parent)
            messages.success(request, 'Private message has been sent.')
            return HttpResponseRedirect(reverse('outbox'))

    else:
        form = PrivateMessageComposeForm(initial={
            'message': "<blockquote>RE: <strong>{user}</strong><br>{msg}</blockquote><br>"
                .format(user=parent.sender, msg=parent.message),
            'subject': 'RE: {subject}'.format(subject=parent.subject),
            'recipient': parent.sender
            })

    return render_to_response('pms/compose_message.html', {
            'form': form,
        }, context_instance=RequestContext(request))

@login_required
def inbox(request):
    messages = PrivateMessage.objects.inbox_for(request.user)
    messages = mk_paginator(request, messages, 50)

    return render_to_response("pms/private_messages.html", 
        add_csrf(request, p_messages=messages, typ="inbox"), 
        context_instance=RequestContext(request))

@login_required
def outbox(request):
    messages = PrivateMessage.objects.outbox_for(request.user)
    messages = mk_paginator(request, messages, 50)

    return render_to_response("pms/private_messages.html", 
        add_csrf(request, p_messages=messages, typ="outbox"), 
        context_instance=RequestContext(request))

@login_required
def archive(request):
    messages = PrivateMessage.objects.archive_for(request.user)
    messages = mk_paginator(request, messages, 50)

    return render_to_response("pms/private_messages.html", 
        add_csrf(request, p_messages=messages, typ="archive"), 
        context_instance=RequestContext(request))

@login_required
def view(request, message_id, slug):
    message = get_object_or_404(PrivateMessage, pk=message_id)

    if message.recipient != request.user and message.sender != request.user:
        raise Http404

    if message.new and message.sender != request.user:
        message.read_at = timezone.now()
        message.save()

    return render_to_response("pms/private_message.html", 
        add_csrf(request, message=message), 
        context_instance=RequestContext(request))

@login_required
def mark_read(request, message_id):
    message = get_object_or_404(PrivateMessage, pk=message_id)

    if message.recipient != request.user or message.sender == request.user:
        raise Http404

    if message.new:
        message.read_at = timezone.now()
        message.save()

    return HttpResponseRedirect(reverse('inbox'))

@login_required
def delete(request, message_id):
    message = get_object_or_404(PrivateMessage, pk=message_id)
    deleted = False
    user = request.user

    if message.sender == user:
        message.sender_deleted_at = timezone.now()
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = timezone.now()
        deleted = True
    if deleted:
        message.save()
        messages.success(request, 'Messages successfully deleted!')

    return HttpResponseRedirect(reverse('inbox'))

@login_required
def undelete(request, message_id):
    message = get_object_or_404(PrivateMessage, pk=message_id)
    undeleted = False
    user = request.user

    if message.sender == user:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.save()
        messages.success(request, 'Messages successfully restored!')

    return HttpResponseRedirect(reverse('inbox'))
