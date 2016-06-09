from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.context_processors import csrf
from .forms import NewPostForm
from django.contrib.auth.decorators import user_passes_test

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