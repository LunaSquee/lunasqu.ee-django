from django.contrib import admin
from forum.models import Section, Forum, Topic, Post, ProfaneWord

class SectionAdmin(admin.ModelAdmin):
    list_display = ["title"]

class ForumAdmin(admin.ModelAdmin):
    list_display = ["title"]

class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created"]
    list_filter = ["forum", "creator"]

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator"]
    list_display = ["title", "topic", "creator", "created"]

class ProfaneWordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Section, SectionAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ProfaneWord, ProfaneWordAdmin)
