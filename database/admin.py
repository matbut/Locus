from django.contrib import admin

from database.models import ImportedArticle, ResultArticle

admin.site.register(ImportedArticle)
admin.site.register(ResultArticle)
