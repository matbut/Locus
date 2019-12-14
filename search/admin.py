from django.contrib import admin

from search.models import SearchParameters
from twitter.models import TwitterUser

admin.site.register(SearchParameters)
admin.site.register(TwitterUser)
