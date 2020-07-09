from django.contrib import admin

# Register your models here.
from posts.models import Post, Comment, PostLike


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'user']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'post', 'user', 'created_at']


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', ]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostLike, PostLikeAdmin)
