from django.contrib.auth import get_user_model, authenticate
# Create your views here.
from rest_framework import viewsets, status, exceptions, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from members.models import Relations, Profile
from members.permissions import IsOwnerOrReadOnly
from members.serializers import UserSerializers, RelationSerializers, UserCreateSerializer, ProfileUpdateSerializer, \
    ChangePassSerializers

User = get_user_model()


class UserModelViewAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['makeFollow', 'makeBlock', 'create_delete_Relation']:
            return RelationSerializers
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'set_password':
            return ChangePassSerializers
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(
            context={'request': self.request}
        )

    @action(detail=True, methods=['post'], url_path='change-password')
    def set_password(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, user)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed('No such user')
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
        # 내가 팔로우를 건 유저
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
    def makeBlock(self, request):
        to_user = User.objects.get(pk=request.query_params.get('toUser'))
        relation_type = request.query_params.get('type')
        try:
            relation = Relations.objects.get(from_user=request.user, to_user=to_user)
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
        relation.related_type = 'b'
        relation.save()
        return Response({'message': 'change relation'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def deleteBlock(self, request):
        to_user = User.objects.get(pk=request.query_params.get('toUser'))
        try:
            relation = Relations.objects.get(from_user=request.user, to_user=to_user)
        except Relations.DoesNotExist:
            return Response({'message: has not Relation'}, status=status.HTTP_400_BAD_REQUEST)
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, methods=['post', 'delete', 'patch'])
    def create_delete_Relation(self, request):
        """
        :param request: relation type 이 f면 팔로우 해주고  b면 블락건다.
        1. 이미 팔로우 한 유저가 블락을 걸면 이미 존재하는 릴레이션 지우고 사용자의 요청에 맞게 해준다.
        """
        to_user = User.objects.get(pk=request.query_params.get('toUser'))
        relation_type = request.query_params.get('type')
        method = request._request.method
        data = {
            'from_user': request.user.pk,
            'to_user': to_user.pk,
            'related_type': relation_type
        }
        try:
            relation = Relations.objects.get(from_user=request.user, to_user=to_user)
            if method == 'PATCH':
                serializers = self.get_serializer(relation, data=data, )
                if serializers.is_valid():
                    serializers.save()
                    return Response(serializers.data, status=status.HTTP_200_OK)
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            elif method == 'DELETE':
                relation.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "올바르지 않은 요청입니다."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Relations.DoesNotExist:
            if method == 'POST':
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserProfileView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet, mixins.ListModelMixin, ):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer

    def get_queryset(self):
        if self.action in ['retrieve', 'partial_update']:
            qs = Profile.objects.filter(pk=self.kwargs['pk'])
        elif self.action == 'list':
            qs = Profile.objects.filter(user=self.request.user)
        return qs
