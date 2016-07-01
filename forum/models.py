from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.template.defaultfilters import slugify

class Section(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, default='')
    priority = models.IntegerField(default=1)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Section, self).save(*args, **kwargs)

    def forums(self):
        return Forum.objects.filter(section=self)

class Forum(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField()
    created = models.DateTimeField(editable=False)
    creator = models.ForeignKey(User, blank=True, null=True)
    closed = models.BooleanField(blank=True, default=False)
    section = models.ForeignKey(Section)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()

        self.slug = slugify(self.title)

        return super(Forum, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def num_topics(self):
        return len(self.topic_set.all())

    def num_posts(self):
        return sum([t.num_posts() for t in self.topic_set.all()])

    def last_post(self):
        if self.topic_set.count():
            last = None
            for t in self.topic_set.all():
                l = t.last_post()
                if l:
                    if not last: last = l
                    elif l.created > last.created: last = l
            return last

    class Meta(object):
        permissions = (
            ("can_lock_forum", "Can change forum lock status"),
            ("can_post_lock_forum", "Can post in locked forums"),
        )

class Topic(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(max_length=10000, blank=True, null=True)
    forum = models.ForeignKey(Forum)
    created = models.DateTimeField(editable=False)
    creator = models.ForeignKey(User, blank=True, null=True)
    updated = models.DateTimeField()
    closed = models.BooleanField(blank=True, default=False)
    pinned = models.BooleanField(blank=True, default=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()

        self.slug = slugify(self.title)

        return super(Topic, self).save(*args, **kwargs)

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return self.post_set.count()

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("-created")[0]

    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title

    class Meta(object):
        permissions = (
            ("can_close_topic", "Can change topic closed status"),
            ("can_pin_topic", "Can change topic pinned status"),
        )

class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(editable=False)
    creator = models.ForeignKey(User, blank=True, null=True)
    updated = models.DateTimeField()
    topic = models.ForeignKey(Topic)
    body = models.TextField(max_length=10000)
    user_ip = models.GenericIPAddressField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.topic, self.title)

    def short(self):
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%b %d, %H:%M"))

    def is_modified(self):
        if self.updated.replace(microsecond=0) > self.created.replace(microsecond=0):
            return True
        return False

    short.allow_tags = True


class ProfaneWord(models.Model):
    word = models.CharField(max_length=60)

    def __unicode__(self):
        return self.word
