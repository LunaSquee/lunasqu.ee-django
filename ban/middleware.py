from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from django.conf import settings

from .models import DeniedIP, AllowedIP

METHODS = getattr(settings, 'BAN_METHODS', ('POST',))
WHITELIST = getattr(settings, 'BAN_WHITELIST', ())
VIEW = getattr(settings, 'BAN_VIEW', 'ban/403.html')

def ip_in_model(ip, model):
    try:
        for i in model.objects.all():
            if ip in i.network():
                return True
    except ValueError:
        pass
    return False

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def forbid(request):
    """
    Forbids a user to access the site
    Cleans up their session (if it exists)
    Returns a templated HttpResponseForbidden when banning requests
    """
    for k in request.session.keys():
        del request.session[k]
    return HttpResponseForbidden(render_to_string(VIEW, context_instance=RequestContext(request)))
    
class DenyMiddleware(object):
    """
    Forbids any request if they are in the DeniedIP list
    """
    def process_request(self, request):
        ip = get_ip(request)
        if not request.method in METHODS or ip in WHITELIST:
            return
        if ip_in_model(ip, DeniedIP):
            return forbid(request)

class AllowMiddleware(object):
    """
    Forbids any request if they are not in the AllowedIP list
    """
    def process_request(self, request):
        if not request.method in METHODS:
            return        
        if not ip_in_model(get_ip(request), AllowedIP):
            return forbid(request)
