from datetime import timedelta

from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from stories.models import Story
from stories.serializers import StorySerializers

User = get_user_model()


class StoryAPIView(ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        qs = User.objects.filter(to_users_relation__from_user=self.request.user,
                                 to_users_relation__related_type='f').values_list('id').distinct()
        time_var = timezone.now() - timedelta(hours=24)
        # Q() 와 filter(, ) 의 차이
        queryset = Story.objects.filter(user_id__in=qs, created_at__gte=time_var)
        return queryset
