from django.contrib.auth.models import User
from django import forms
from .models import PrivateMessage
from django.utils import timezone
from personal.bleach import bleach_clean

class PrivateMessageComposeForm(forms.Form):
    recipient = forms.CharField(max_length=30, label=u'Recipient', help_text="Currently only supports a single recipient.")
    subject = forms.CharField(max_length=120, label=u'Subject')
    message = forms.CharField(label=u'Message', widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))

    def clean_recipient(self):
        try:
            recipient = User.objects.get(username=self.cleaned_data['recipient'])
        except User.DoesNotExist:
            raise forms.ValidationError(u'That user does not exist!', code='invalid')

        return recipient

    def save(self, sender, parent=None):
        recipient = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        message = bleach_clean(self.cleaned_data['message'])

        msg = PrivateMessage(sender=sender, recipient=recipient, subject=subject, message=message)
        if parent is not None:
            msg.parent_msg = parent
            parent.replied_at = timezone.now()
            parent.save()
        msg.save()

        return msg
