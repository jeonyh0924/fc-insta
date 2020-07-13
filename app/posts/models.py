import factory
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F
from factory import Factory

User = get_user_model()


def post_image_path(instance, filename):
    path = f'{instance.id}/{filename}'
    return path


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
    like_count = models.IntegerField(default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super().save()


class PostImage(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        null=True,
    )
    image = models.ImageField(
        upload_to=post_image_path,
    )


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
    like_count = models.IntegerField(default=0)


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

    class Meta:
        unique_together = ['user', 'post']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        post = Post.objects.get(id=self.post.id)
        post.like_count = F('like_count') + 1
        post.save()
        return super().save()


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
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('user', 'comment')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        comment = Comment.objects.filter(id=self.comment_id)
        comment.update(like_count=F('like_count') + 1)
        return super().save()


class PostFactory(Factory):
    class Meta:
        model = PostImage

    image = factory.django.ImageField(color='blue')
