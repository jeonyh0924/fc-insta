from django.urls import path
from rest_framework import routers

from members.views import UserModelViewAPI, RelationAPIView

router = routers.SimpleRouter(trailing_slash=False)
router.register('relation', RelationAPIView)
router.register(r'user', UserModelViewAPI)

urlpatterns = router.urls
