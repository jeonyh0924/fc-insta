from rest_framework import serializers

from members.serializers import UserSerializers, UserSimpleSerializers
from posts.models import Post, Comment, PostLike, CommentLike, PostImage


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializers(serializers.ModelSerializer):
    child = RecursiveField(many=True, required=False)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'user', 'parent', 'child', 'like_count')


class CommentUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content',)


class PostImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image')


class PostSerializers(serializers.ModelSerializer):
    """
    전체 게시글에 대해서 유저
    """
    images = PostImageSerializers(many=True, read_only=True, )
    comment = CommentSerializers(many=True, read_only=True, )
    user = UserSimpleSerializers(read_only=True, )

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'images', 'comment', 'like_count')
        read_only_fields = ('like_count',)

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


class PostProfileSerializers(serializers.ModelSerializer):
    images = PostImageSerializers(many=True, )
    user = UserSerializers()
    comment = CommentSerializers(many=True, read_only=True, )

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'created_at', 'like_count', 'images', 'comment',)


class PostLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('id', 'post', 'user')


class CommentLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user')
