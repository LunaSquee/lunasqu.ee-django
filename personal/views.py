from .forms import ResendActivationEmailForm, SettingsForm
from .helpers import mk_paginator, add_csrf
from django.http import HttpResponseRedirect, Http404
from django.core import signing
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.conf import settings

def index(request):
    return render(request, 'personal/index.html')

def about(request):
    return render(request, 'personal/about.html')

def view_profile(request, **kwargs):
    context = {}

    username = kwargs.get('username')
    if username:
        context['profile'] = get_object_or_404(User, username=username)
    elif request.user.is_authenticated():
        context['profile'] = request.user
    else:
        raise Http404  # Case where user gets to this view anonymously for non-existent user

    return render(request, 'registration/profile.html', context)

@login_required
def edit_settings(request, **kwargs):
    user = request.user
    form = SettingsForm(initial={'email': request.user.email}, instance=request.user.profile)

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user.profile)

        if form.has_changed():
            if form.is_valid():
                up = form.save(commit=False)
                up.user = request.user
                up.save()

                email = form.cleaned_data['email']
                user.email = email
                user.save()

                messages.success(request, 'Profile details updated.')

    return render_to_response('registration/settings.html', {
            'form': form,
            'profile': request.user.profile,
        }, context_instance=RequestContext(request))

def resend_activation_email(request):

    email_body_template = 'registration/activation_email.txt'
    email_subject_template = 'registration/activation_email_subject.txt'

    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')

    context = {}

    form = None
    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email, is_active=0)

            if not users.count():
                form._errors["email"] = ["This email is not registered or already activated."]

            REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT', 'registration')
            for user in users:
                activation_key = signing.dumps(
                    obj=getattr(user, user.USERNAME_FIELD),
                    salt=REGISTRATION_SALT,
                    )
                context = {}
                context['activation_key'] = activation_key
                context['expiration_days'] = settings.ACCOUNT_ACTIVATION_DAYS
                context['site'] = get_current_site(request)

                subject = render_to_string(email_subject_template, context)
                # Force subject to a single line to avoid header-injection
                # issues.
                subject = ''.join(subject.splitlines())
                message = render_to_string(email_body_template, context)
                user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
                return render(request, 'registration/resend_activation_email_done.html')

    if not form:
        form = ResendActivationEmailForm()

    context = {"form" : form}
    return render(request, 'registration/resend_activation_email_form.html', context)
