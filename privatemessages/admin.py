from django.contrib import admin
from .models import PrivateMessage

class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ["subject"]

admin.site.register(PrivateMessage, PrivateMessageAdmin)
