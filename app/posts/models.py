from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Post(models.Model):
    title = models.CharField('글 제목', max_length=20, )
    content = models.CharField('글 내용', max_length=50)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Comment(models.Model):
    content = models.CharField(
        '댓글 내용',
        max_length=100,
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class PostLike(models.Model):
    pass
