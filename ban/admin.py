from django.conf import settings
from django.contrib import admin
from .models import DeniedIP, AllowedIP

class IPAdmin(admin.ModelAdmin):
    search_fields = ('ip',)

if 'ban.middleware.DenyMiddleware' in settings.MIDDLEWARE_CLASSES:
    admin.site.register(DeniedIP, IPAdmin)

if 'ban.middleware.AllowMiddleware' in settings.MIDDLEWARE_CLASSES:
    admin.site.register(AllowedIP, IPAdmin)