from rest_framework import serializers

from posts.models import Post, Comment


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'image', 'user')

    def create(self, validated_data):
        return super().create(validated_data)


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'user')
