from django.conf.urls import url
from django.urls import include, path
from rest_framework_nested import routers

from members.views import UserModelViewAPI, UserProfileView
from posts.views import PostsAPIView, CommentAPIView, PostLikeAPIView, CommentLikeAPIView

router = routers.SimpleRouter(trailing_slash=True)
router.register('users', UserModelViewAPI)
router.register('posts', PostsAPIView)
# router.register('like', PostLikeAPIView)
users_router = routers.NestedSimpleRouter(router, 'users')
post_like_router = routers.NestedSimpleRouter(router, 'posts')
post_like_router.register('like', PostLikeAPIView)
post_like_router.register('comments', CommentAPIView)

comment_like_router = routers.NestedSimpleRouter(post_like_router, 'comments')
comment_like_router.register('like', CommentLikeAPIView)

users_router.register('posts', PostsAPIView)
users_router.register('profile', UserProfileView)
posts_router = routers.NestedSimpleRouter(users_router, 'posts')
posts_router.register('comments', CommentAPIView)
posts_router.register('like', PostLikeAPIView)

urlpatterns = [
    url('', include(router.urls)),
    url('', include(users_router.urls)),
    url('', include(post_like_router.urls)),
    url('', include(posts_router.urls)),
    url('', include(comment_like_router.urls)),
]
