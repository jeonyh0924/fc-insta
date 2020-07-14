from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Post, Comment, PostLike, CommentLike
from posts.serializers import PostSerializers, CommentSerializers, CommentUpdateSerializers, PostUpdateSerializers, \
    PostLikeSerializers, CommentLikeSerializers, CommentListSerializers

User = get_user_model()


class PostsAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return PostUpdateSerializers
        elif self.action == 'list':
            return PostSerializers
        return super().get_serializer_class()

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
        elif self.action == 'list':
            return CommentListSerializers
        else:
            return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        try:
            self.request.data.get('parent')
            model = self.queryset.model
            ins = model.objects.get(pk=self.request.data['parent'])
            # parent 의 부모가 있다면, 올바르지 않은 생성 - 대대댓글이 된다.
            if ins.parent:
                # raise Exception('depth of comments is only level 2')
                return Response(
                    {'message': 'depth of comments is only level 2'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except MultiValueDictKeyError:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            post=Post.objects.get(pk=self.kwargs['nested_2_pk'])
        )


class PostLikeAPIView(GenericViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializers

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            post=Post.objects.get(pk=self.kwargs['nested_2_pk'])
        )

    @action(detail=False, methods=['post'], url_path='toggle')
    def like_toggle(self, request, **kwargs):
        try:
            like = PostLike.objects.get(
                user=request.user,
                post=Post.objects.get(pk=self.kwargs['nested_2_pk'])
            )
            like.delete()
            return Response(
                {'message': 'post like delete'},
                status=status.HTTP_204_NO_CONTENT
            )
        except PostLike.DoesNotExist:
            data = {
                'post': Post.objects.get(pk=self.kwargs['nested_2_pk']).pk,
                'user': request.user.pk
            }
            serializers = PostLikeSerializers(data=data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)


class CommentLikeAPIView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializers

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user.id,
            comment=Comment.objects.get(pk=self.kwargs['nested_1_pk']).pk
        )

    @action(detail=False, methods=['post'], url_path='toggle')
    def like_toggle(self, request, **kwargs):
        try:
            like = CommentLike.objects.get(
                user=request.user,
                comment=Comment.objects.get(pk=self.kwargs['nested_2_pk'])
            )
            like.delete()
            return Response(
                {'message': 'post like delete'},
                status=status.HTTP_204_NO_CONTENT
            )
        except CommentLike.DoesNotExist:
            data = {
                'comment': Comment.objects.get(pk=self.kwargs['nested_2_pk']).pk,
                'user': request.user.pk
            }
            serializers = self.get_serializer(data=data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
