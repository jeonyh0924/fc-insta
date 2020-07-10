from django.conf.urls import url
from django.urls import include
from rest_framework_nested import routers

from members.views import UserModelViewAPI, UserProfileView
from posts.views import PostsAPIView, CommentAPIView, PostLikeAPIView

router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UserModelViewAPI)
users_router = routers.NestedSimpleRouter(router, 'users')
users_router.register('posts', PostsAPIView)
users_router.register('profile', UserProfileView)
posts_router = routers.NestedSimpleRouter(users_router, 'posts')
posts_router.register('comments', CommentAPIView)
posts_router.register('like', PostLikeAPIView)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'', include(users_router.urls)),
    url('', include(posts_router.urls)),
]
