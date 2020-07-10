from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from django.test import TestCase

# Create your tests here.
from rest_framework import views, viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from posts.models import Post, Comment, PostLike, CommentLike
from posts.serializers import PostSerializers, CommentSerializers, CommentUpdateSerializers, PostUpdateSerializers, \
    PostLikeSerializers, CommentLikeSerializers

User = get_user_model()


class PostsAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return PostUpdateSerializers
        return super().get_serializer_class()

    def get_queryset(self):
        qs = Post.objects.filter(user=User.objects.first())
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return CommentUpdateSerializers
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            post=Post.objects.get(pk=self.kwargs['nested_2_pk'])
        )


class PostLikeAPIView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post=Post.objects.get(pk=self.kwargs['nested_2_pk']))


class CommentLikeAPIView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializers
