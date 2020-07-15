from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, mixins, status, serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Post, Comment, PostLike, CommentLike
from posts.serializers import PostSerializers, CommentUpdateSerializers, PostUpdateSerializers, PostLikeSerializers, \
    CommentLikeSerializers, CommentSerializers

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
            return CommentSerializers
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        """
        댓글 작성
        - parent와 post는 공존 할 수 없다. ( comment Serializers 에 의해)
        - parent 만 오는 주소와 /comment/<comment:pk>  kwargs 'comment_pk'
        - post 만 오는 주소를 /posts/<post:pk>        kwargs 'post_pk'
        - 구분을 지어야 한다.
        - 둘 다 통합 처리하면 클라이언트에서 알아보기 힘듬

        -
        """
        if 'comment_pk' in self.kwargs:
            comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
            serializer.save(
                user=self.request.user,
                parent=comment
            )
        elif 'post_pk' in self.kwargs:
            post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
            serializer.save(
                user=self.request.user,
                post=post
            )
        else:
            raise serializers.ValidationError('대댓글만 작성 가능')

        # serializer.save(
        #     user=self.request.user,
        #     post=Post.objects.get(pk=self.kwargs['post_pk'])
        # )


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
                post=Post.objects.get(pk=self.kwargs['post_pk'])
            )
            like.delete()
            return Response(
                {'message': 'post like delete'},
                status=status.HTTP_204_NO_CONTENT
            )
        except PostLike.DoesNotExist:
            data = {
                'post': Post.objects.get(pk=self.kwargs['post_pk']).pk,
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
                comment=Comment.objects.get(pk=self.kwargs['comment_pk'])
            )
            like.delete()
            return Response(
                {'message': 'post like delete'},
                status=status.HTTP_204_NO_CONTENT
            )
        except CommentLike.DoesNotExist:
            data = {
                'comment': Comment.objects.get(pk=self.kwargs['comment_pk']).pk,
                'user': request.user.pk
            }
            serializers = self.get_serializer(data=data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
