from django.urls import path
from rest_framework import routers

from members.views import UserModelViewAPI, UserProfileView

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'user', UserModelViewAPI)
router.register('profile', UserProfileView)

urlpatterns = router.urls
