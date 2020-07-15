from rest_framework import serializers

from members.serializers import UserSerializers
from posts.models import Post, Comment, PostLike, CommentLike, PostImage


class CommentSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'user')


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentListSerializers(serializers.ModelSerializer):
    child = RecursiveField(many=True, required=False)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'user', 'parent', 'child')


class CommentUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content',)


class PostImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image')


class PostSerializers(serializers.ModelSerializer):
    images = PostImageSerializers(many=True, read_only=True, )
    comment = CommentListSerializers(many=True, read_only=True, )
    user = UserSerializers(read_only=True, )

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'images', 'comment')

    def create(self, validated_data):
        posts_image = self.context['request'].FILES
        post = Post.objects.create(**validated_data)
        for image in posts_image.getlist('images'):
            PostImage.objects.create(post=post, image=image)
        return post


class PostUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content')


class PostLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('id', 'post', 'user')


class CommentLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user')
