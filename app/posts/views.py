from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from django.test import TestCase

# Create your tests here.
from rest_framework import views, viewsets

from posts.models import Post
from posts.serializers import PostSerializers

User = get_user_model()


class PostsAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def get_queryset(self):
        qs = Post.objects.filter(user=User.objects.first())
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
