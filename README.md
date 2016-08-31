# lunasqu.ee-django

## Installing: 

1. `$ git clone https://github.com/LunaSquee/lunasqu.ee-django.git && cd lunasqu.ee-django`
2. `$ sudo pip install -r requirements.txt`
3. `$ django-admin startproject lunasquee .`
4. Install and run `memcached` on your server.

Edit the settings file. **Requirements: **


```
INSTALLED_APPS = [
    'blog',
    'forum',
    'personal',
    'ban',
    'privatemessages',
    ...
]

MIDDLEWARE_CLASSES = [
    'ban.middleware.DenyMiddleware',
    'forum.middleware.PageViewsMiddleware',
    'personal.middleware.ActiveUserMiddleware',
    ...
]

ROOT_URLCONF = 'urls'

ACCOUNT_ACTIVATION_DAYS = 2

LOGIN_REDIRECT_URL = "/"

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "usercontent/")

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Number of seconds of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 300

# Number of seconds that we will keep track of inactive users for before 
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7
```

Along with a working EMAIL backend for account verification.
