from django.db.models import F
from rest_framework import serializers

from members.serializers import UserSerializers, UserSimpleSerializers, UserProfileSerializers
from posts.models import Post, Comment, PostLike, CommentLike, PostImage, Tag


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializers(serializers.ModelSerializer):
    user = UserProfileSerializers(read_only=True)
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


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'count')


class PostSerializers(serializers.ModelSerializer):
    """
    전체 게시글에 대해서 유저
    """
    images = PostImageSerializers(many=True, read_only=True, )
    comment = CommentSerializers(many=True, read_only=True, )
    user = UserSimpleSerializers(read_only=True, )
    tags = TagSerializers(many=True, read_only=True, )
    tags_list = serializers.ListField(
        child=serializers.CharField(max_length=20), write_only=True,
    )

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'images', 'comment', 'like_count', 'tags', 'tags_list')
        read_only_fields = ('like_count',)

    def create(self, validated_data):
        tags = validated_data.pop('tags_list')
        posts_image = self.context['request'].FILES
        post = Post.objects.create(**validated_data)
        for image in posts_image.getlist('images'):
            PostImage.objects.create(post=post, image=image)
        for name in tags:
            ins, __ = Tag.objects.get_or_create(name=name)
            post.tags.add(ins)
            ins.count = F('count') + 1
            ins.save()
        return post


class PostUpdateSerializers(serializers.ModelSerializer):
    tags = TagSerializers(many=True, read_only=True, )

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'tags',)


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
