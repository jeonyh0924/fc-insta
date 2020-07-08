from django.shortcuts import render

# Create your views here.
from django.test import TestCase

# Create your tests here.
from rest_framework import views, viewsets

from posts.models import Post
from posts.serializers import PostSerializers


class PostsAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def perform_create(self, serializer):
        serializer.save()