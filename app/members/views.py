import time

from django.contrib.auth import get_user_model, authenticate
# Create your views here.
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status, exceptions, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from members.models import Relations, Profile, RecentlyUser
from members.permissions import IsOwnerOrReadOnly
from members.serializers import UserSerializers, RelationSerializers, UserCreateSerializer, ProfileUpdateSerializer, \
    ChangePassSerializers, ProfileDetailSerializers, UserSimpleSerializers, RecentlyUserSerializers, \
    UserProfileSerializers
from posts.models import Post
from posts.serializers import PostProfileSerializers, PostSerializers
from django.core.cache import cache

User = get_user_model()


# def retrieve_get_object(self):
#     """
#     Returns the object the view is displaying.
#
#     You may want to override this if you need to provide non-standard
#     queryset lookups.  Eg if objects are referenced using multiple
#     keyword arguments in the url conf.
#     """
#     queryset = self.filter_queryset(self.get_queryset()).cache()
#
#     # Perform the lookup filtering.
#     lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
#
#     assert lookup_url_kwarg in self.kwargs, (
#             'Expected view %s to be called with a URL keyword argument '
#             'named "%s". Fix your URL conf, or set the `.lookup_field` '
#             'attribute on the view correctly.' %
#             (self.__class__.__name__, lookup_url_kwarg)
#     )
#
#     filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
#     obj = get_object_or_404(queryset, **filter_kwargs)
#
#     # May raise a permission denied
#     self.check_object_permissions(self.request, obj)
#
#     return obj


class UserModelViewAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_queryset(self):
        queryset = super().get_queryset().select_related('profile')
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = User.objects.filter(profile__username__startswith=username).select_related('profile')
        return queryset

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserProfileSerializers
        if self.action in ['makeFollow', 'makeBlock', 'create_delete_Relation']:
            return RelationSerializers
        elif self.action in ['create', 'login']:
            return UserCreateSerializer
        elif self.action == 'set_password':
            return ChangePassSerializers
        elif self.action in ['partial_update', 'retrieve']:
            return UserSimpleSerializers
        return super().get_serializer_class()

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset()).cache()
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     key = f"user{kwargs['pk']}"
    #     instance = cache.get(key)
    #     if not instance:
    #         instance = self.get_object()
    #         cache.set(key, instance, 60 * 60)
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='change-password')
    def set_password(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, user)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False)
    def page(self, request):
        # 내가 팔로우를 건 유저들의 게시글
        qs = User.objects.filter(Q(to_users_relation__from_user=request.user,
                                   to_users_relation__related_type='f') |
                                 Q(pk=request.user.pk)
                                 )
        posts = Post.objects.filter(user_id__in=qs).select_related('user__profile') \
            .prefetch_related('comment__user__profile', 'images', 'comment__child__parent')
        serializers = PostProfileSerializers(posts, many=True, context=request)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False, )
    def myProfile(self, request):
        # 내가 쓴 게시글
        posts = Post.objects.filter(user=request.user).select_related('user', ) \
            .prefetch_related('comment__user__profile', 'tags', 'images', 'comment__child__parent')
        serializers = PostSerializers(posts, many=True, context=request)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed('No such user')

        token_key = 'here_is_token'
        token_value = cache.get(token_key)
        if not token_value:
            old_token = Token.objects.filter(user=user)
            if old_token.exists():
                old_token.delete()
            token_value, __ = Token.objects.get_or_create(user=user)
            cache.set(token_key, token_value, 60 * 60 * 24)
        data = {
            'token': token_value.key
        }
        return Response(data, status=status.HTTP_201_CREATED)

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
        serializer = UserSerializers(users, many=True, context=self.request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def follower(self, request):
        users = request.user.follower
        serializers = UserSerializers(users, many=True, context=self.request)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def block(self, request):
        users = request.user.block
        serializers = UserSerializers(users, many=True, context=self.request)
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


class UserProfileView(mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet, ):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer

    def get_queryset(self):
        if self.action in ['retrieve', 'partial_update']:
            qs = Profile.objects.filter(pk=self.kwargs['pk']).select_related('user')

        # elif self.action == 'list':
        #     qs = Profile.objects.filter(user=self.request.user).select_related('user').cache()
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProfileDetailSerializers
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = retrieve_get_object(self)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RelationAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Relations.objects.all()
    serializer_class = RelationSerializers

    """
    릴레이션이 생성이 될 때, F면 +1 B은 영향을 주지 않는다.
            삭제가 될 때 F면 -1 B은 영향을 주지 않는다.
    """

    def create(self, request, *args, **kwargs):
        to_user = User.objects.get(pk=kwargs['user_pk'])
        data = {
            "from_user": request.user.id,
            "to_user": to_user.id,
            "related_type": request.data['related_type']
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer.save()


class RecentlyUserAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = RecentlyUser.objects.all()
    serializer_class = RecentlyUserSerializers

    def get_queryset(self):
        if self.kwargs['user_pk']:
            qs = User.objects.filter(recently_to_user__from_user=self.kwargs['user_pk'])
            queryset = Profile.objects.filter(user__id__in=qs)
            return queryset
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileDetailSerializers
        return super().get_serializer_class()

    def perform_create(self, serializer):
        """
        2개 이상이면 가장 오래된 기록 삭제
        """
        to_user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        if to_user:
            serializer.save(from_user=self.request.user, to_user=to_user)
