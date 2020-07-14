from django.contrib import admin

# Register your models here.
from posts.models import Post, Comment, PostLike, CommentLike


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'user']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'post', 'user', 'created_at', 'like_count']


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', ]


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comment']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
