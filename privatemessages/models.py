from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone

class MessageManager(models.Manager):

    def inbox_for(self, user):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
        )

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )

    def archive_for(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
        )

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name="send", blank=True, null=True)
    recipient = models.ForeignKey(User, related_name="recieve", blank=True, null=True)
    parent_msg = models.ForeignKey('self', related_name="parent", blank=True, null=True)
    subject = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    message = models.TextField(blank=True, default='')
    sent_at = models.DateTimeField("sent at", blank=True, null=True)
    read_at = models.DateTimeField("read at", blank=True, null=True)
    replied_at = models.DateTimeField("replied at", blank=True, null=True)
    sender_deleted_at = models.DateTimeField("Sender deleted at", null=True, blank=True)
    recipient_deleted_at = models.DateTimeField("Recipient deleted at", null=True, blank=True)

    objects = MessageManager()

    def replied(self):
        if self.replied_at is not None:
            return True
        return False

    def new(self):
        if self.read_at is not None:
            return False
        return True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.sent_at = timezone.now()

        self.slug = slugify(self.subject)

        return super(PrivateMessage, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.subject

    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Private Message"
        verbose_name_plural = "Private Messages"

def count_unread(user):
    return PrivateMessage.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()
