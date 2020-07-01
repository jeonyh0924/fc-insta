from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from members.serializers import UserSerializers

User = get_user_model()


class UserModelViewAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
            data = {
                'message': 'token create',
                'token': token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            'message': 'token get',
            'token': token.key,
        }
        return Response(data, status=status.HTTP_200_OK)
