from django.contrib.auth import get_user_model, authenticate
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from members.models import Relations
from members.serializers import UserSerializers, RelationSerializers

User = get_user_model()


class UserModelViewAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'makeFollow':
            return RelationSerializers
        return super().get_serializer_class()

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

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        user = request.user
        if user.auth_token:
            user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def follow(self, request):
        users = request.user.follow
        serializer = UserSerializers(users, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def follower(self, request):
        users = request.user.follower
        serializers = UserSerializers(users, many=True, )
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def block(self, request):
        users = request.user.block
        serializers = UserSerializers(users, many=True, )
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def makeFollow(self, request):
        to_user = User.objects.get(pk=request.query_params.get('toUser'))
        relation_type = request.query_params.get('type')
        try:
            Relations.objects.get(from_user=request.user, to_user=to_user)
        except Relations.DoesNotExist:
            data = {
                'from_user': request.user.pk,
                'to_user': to_user.pk,
                'related_type': relation_type
            }
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "exists relation"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def deleteFollow(self, request):
        try:
            relation = Relations.objects.get(from_user=request.user,
                                             to_user=User.objects.get(pk=request.query_params.get('toUser')))
            relation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Relations.DoesNotExist:
            return Response({'message': " not exists relation"}, status=status.HTTP_400_BAD_REQUEST)


class RelationAPIView(viewsets.ModelViewSet):
    queryset = Relations.objects.all()
    serializer_class = RelationSerializers
