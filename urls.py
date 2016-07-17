"""lunasquee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from personal import views
from django.conf.urls.static import static
from personal.forms import MyRegistrationForm
from registration.backends.hmac.views import RegistrationView
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^', include('personal.urls')),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^admin/', admin.site.urls),
    url(r'accounts/register/$', 
        RegistrationView.as_view(form_class = MyRegistrationForm), 
        name = 'registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/resend_email/', views.resend_activation_email, name="resend_activation_email"),
    url(r'^accounts/profile/$', views.view_profile, name="view_profile"),
    url(r'^accounts/profile/(?P<username>\w+)/$', views.view_profile, name="view_other_profile"),
    url(r'^accounts/settings/$', views.edit_settings, name="edit_settings"),
    url(r'^blog/', include('blog.urls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^inbox/', include('privatemessages.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.err404
handler500 = views.err500