from django.db import models
from django.contrib.auth.models import User
from forum.models import Topic, Post
from privatemessages.models import count_unread
from django.core.cache import cache 
import datetime
import time
import uuid
from lunasquee import settings
import os

class Badge(models.Model):
    title = models.CharField(max_length=20)
    display = models.CharField(max_length=16)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

def avatar_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s-%s-%s.%s" % (instance.user.id, int(time.time()), uuid.uuid4().hex[:8], ext)
    return os.path.join('profile_images', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_file_name, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)

    def get_topic_count(self):
        return len(Topic.objects.filter(creator=self.user))

    def get_post_count(self):
        return len(Post.objects.filter(creator=self.user))

    def get_avatar(self):
        if not self.avatar:
            return "/static/images/avatar_blank.png"

        return "/media/"+str(self.avatar)

    def displayable_name(self):
        if not self.display_name:
            return self.user.username
        return self.display_name

    def reputation(self):
        return 0

    def __unicode__(self):
        return self.user

    def badges(self):
        return Badge.objects.filter(user=self.user)

    def unreadmsgs(self):
        return count_unread(self.user)

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
