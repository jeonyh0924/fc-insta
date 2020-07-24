from django.conf.urls import url
from django.urls import include
from rest_framework_nested import routers

from members.views import UserModelViewAPI, UserProfileView, RelationAPIView, RecentlyUserAPIView
from posts.views import PostsAPIView, CommentAPIView, PostLikeAPIView, CommentLikeAPIView, TagAPIView
from stories.views import StoryAPIView

router = routers.SimpleRouter(trailing_slash=False)

router.register('users', UserModelViewAPI)
router.register('posts', PostsAPIView)
router.register('comments', CommentAPIView)
router.register('relation', RelationAPIView)
router.register('story', StoryAPIView)
router.register('tag', TagAPIView)

# /users/
users_router = routers.NestedSimpleRouter(router, 'users', lookup='user')
# /users/posts
users_router.register('posts', PostsAPIView)
# /users/profile
users_router.register('profile', UserProfileView)
# /users/relation
users_router.register('relation', RelationAPIView)
# /users/story
users_router.register('story', StoryAPIView)
# /users/recently
users_router.register('recently', RecentlyUserAPIView)

# /users/posts
posts_router = routers.NestedSimpleRouter(users_router, 'posts', lookup='post')
# /users/posts/comments
posts_router.register('comments', CommentAPIView)
# /users/posts/like
posts_router.register('like', PostLikeAPIView)

# /posts
post_like_router = routers.NestedSimpleRouter(router, 'posts', lookup='post')
# /posts/like
post_like_router.register('like', PostLikeAPIView)
# /posts/comments
post_like_router.register('comments', CommentAPIView)

# /comments
comment_router = routers.NestedSimpleRouter(router, 'comments', lookup='comment')
comment_router.register('reply', CommentAPIView)
# /posts/comment/like
comment_like_router = routers.NestedSimpleRouter(post_like_router, 'comments', lookup='comment')
comment_like_router.register('like', CommentLikeAPIView)

urlpatterns = [
    url('', include(router.urls)),
    url('', include(users_router.urls)),
    url('', include(post_like_router.urls)),
    url('', include(posts_router.urls)),
    url('', include(comment_like_router.urls)),
    url('', include(comment_router.urls)),
]
