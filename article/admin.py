from django.contrib import admin
from . models import *
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    summernote_fields = ('content',)
    


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Comment)
admin.site.register(LovedArticle)
admin.site.register(LikedComment)





