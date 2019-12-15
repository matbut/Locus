from django.contrib import admin

from searchEngine.models import InternetResult
from search.models import Domain

admin.site.register(InternetResult)
admin.site.register(Domain)
