from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def story_video(instance, filename):
    return f'video/{instance.user.id}/{filename}'


def story_image(instance, filename):
    return f'storyImage/{instance.story.user_id}/{filename}'


# Create your models here.
class Story(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    content = models.CharField(
        max_length=100,
        null=True,
    )
    video = models.FileField(
        upload_to=story_video,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class StoryImage(models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='image',
    )
    image = models.ImageField(
        upload_to=story_image,
    )


class StoryCheck(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='check_set',
    )
