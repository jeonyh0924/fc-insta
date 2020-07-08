from rest_framework import serializers

from posts.models import Post


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user')
