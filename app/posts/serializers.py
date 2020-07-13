from rest_framework import serializers

from members.serializers import UserSerializers
from posts.models import Post, Comment, PostLike, CommentLike, PostImage


class PostImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('image')


class PostSerializers(serializers.ModelSerializer):
    images = PostImageSerializers(many=True, read_only=True, )

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'images')

    def create(self, validated_data):
        posts_image = self.context['request'].FILES
        post = Post.objects.create(**validated_data)
        for image in posts_image.getlist('image'):
            image = PostImage.objects.create(post=post, image=image)
        return post


class PostUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content')


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
        model = CommentLike
        fields = ('id', 'comment', 'user')
