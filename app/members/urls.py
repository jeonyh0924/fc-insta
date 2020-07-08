from django.conf.urls import url
from django.urls import include
from rest_framework_nested import routers

from members.views import UserModelViewAPI, UserProfileView
from posts.views import PostsAPIView

router = routers.SimpleRouter()
router.register(r'users', UserModelViewAPI)

users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'posts', PostsAPIView)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(users_router.urls)),
]
