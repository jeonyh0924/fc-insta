from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Post(models.Model):
    title = models.CharField('글 제목', max_length=20, )
    content = models.CharField('글 내용', max_length=50, null=True, )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    image = models.ImageField(
        upload_to="%y/%m/%d",
        null=True,
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super().save()


class Comment(models.Model):
    content = models.CharField(
        '댓글 내용',
        max_length=100,
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class PostLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class CommentLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
    )
