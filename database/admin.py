from django.contrib import admin

from database.models import ImportedArticle, ResultArticle, TopWord

admin.site.register(ImportedArticle)
admin.site.register(ResultArticle)
admin.site.register(TopWord)
