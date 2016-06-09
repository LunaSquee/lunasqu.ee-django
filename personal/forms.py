from registration.forms import RegistrationForm
from django.db import models
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.core.files.images import get_image_dimensions

class ResendActivationEmailForm(forms.Form):
    username = forms.CharField(required=True)

class SettingsForm(forms.ModelForm):
    email = forms.EmailField(label=u'Email Address', required=True)
    avatar = forms.ImageField(label=u'Change Avatar', required=False, error_messages={'invalid': 'Image files only'}, widget=forms.FileInput)

    class Meta:
        model = Profile
        exclude = ('user','signature',)

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 2800
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (200 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 200k.')

        except AttributeError:
            pass

        return avatar

class MyRegistrationForm(RegistrationForm):
    display_name = forms.CharField(max_length=20, label=u'Display Name')

    def save(self, *args, **kwargs):
        new_user = super(MyRegistrationForm, self).save(*args, **kwargs)
        new_user.save()

        #create a new profile for this user with his information
        Profile(user=new_user, display_name=self.cleaned_data['display_name']).save()

        #return the User model
        return new_user