from django.contrib import admin

from .models import Tweet, Hashtag

admin.site.register(Hashtag)
admin.site.register(Tweet)
