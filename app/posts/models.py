from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

User = get_user_model()


def post_image_path(instance, filename):
    path = f'{instance.id}/{filename}'
    return path


class Post(models.Model):
    title = models.CharField('글 제목', max_length=50, )
    content = models.CharField('글 내용', max_length=50, null=True, )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    like_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(
        'Tag',
        null=True,
        blank=True,
        related_query_name='posts',
    )


class PostImage(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        null=True,
        related_name='images',
    )
    image = models.ImageField(
        upload_to=post_image_path,
    )


class Comment(MPTTModel):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child',
    )
    content = models.CharField(
        '댓글 내용',
        max_length=100,
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comment',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
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

    def delete(self, using=None, keep_parents=False):
        post = Post.objects.get(id=self.post.id)
        post.like_count = F('like_count') - 1
        post.save()
        return super().delete()


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

    def delete(self, using=None, keep_parents=False):
        comment = Comment.objects.filter(id=self.comment_id)
        comment.update(like_count=F('like_count') - 1)
        return super().delete()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True, )
    count = models.IntegerField(default=0)
