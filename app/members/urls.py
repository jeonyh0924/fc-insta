from django.conf.urls import url
from django.urls import include
from rest_framework_nested import routers

from members.views import UserModelViewAPI, UserProfileView
from posts.views import PostsAPIView

router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UserModelViewAPI)
router.register('profile', UserProfileView)

users_router = routers.NestedSimpleRouter(router, 'users')
users_router.register('posts', PostsAPIView)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'', include(users_router.urls)),
]
