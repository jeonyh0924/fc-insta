from django.contrib import admin

# Register your models here.
from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'user']


admin.site.register(Post, PostAdmin)
