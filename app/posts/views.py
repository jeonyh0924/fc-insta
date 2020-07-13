from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
        serializer.save(user=self.request.user,
                        # context=self.request
                        )

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

    # http://localhost:8000/users/1/posts/1/like/
    @action(detail=False, methods=['post'], url_path='toggle')
    def like_toggle(self, request, **kwargs):
        try:
            like = PostLike.objects.get(user=request.user, post=Post.objects.get(pk=self.kwargs['nested_2_pk']))
            like.delete()
            return Response({'message': 'post like delete'}, status=status.HTTP_204_NO_CONTENT)
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
        serializer.save(user=self.request.user.id, comment=Comment.objects.get(pk=self.kwargs['nested_1_pk']).pk)

    @action(detail=False, methods=['post'], url_path='toggle')
    def like_toggle(self, request, **kwargs):
        try:
            like = CommentLike.objects.get(user=request.user,
                                           comment=Comment.objects.get(pk=self.kwargs['nested_2_pk']))
            like.delete()
            return Response({'message': 'post like delete'}, status=status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            data = {
                'comment': Comment.objects.get(pk=self.kwargs['nested_2_pk']).pk,
                'user': request.user.pk
            }
            serializers = self.get_serializer(data=data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
