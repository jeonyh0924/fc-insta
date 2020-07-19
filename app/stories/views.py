from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from stories.models import Story
from stories.serializers import StorySerializers


class StoryAPIView(ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)