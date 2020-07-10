from rest_framework import serializers

from members.serializers import UserSerializers
from posts.models import Post, Comment, PostLike


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'image', 'user')

    def create(self, validated_data):
        return super().create(validated_data)


class PostUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'image')


class CommentSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'user')


class CommentUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content',)


class PostLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('id', 'post', 'user')


class CommentLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user')
