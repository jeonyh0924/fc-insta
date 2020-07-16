from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from config import settings
from members.models import Profile
from posts.models import Post, Comment, PostLike

User = get_user_model()


class PostTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='testUser@test.com',
            password='1111'
        )
        Profile.objects.create(user=self.user, username='TestUser')
        for i in range(2):
            self.post = Post.objects.create(
                user=self.user,
                title=f'test Post{i}'
            )
        self.url = f'/users/{self.user.id}/posts'

    def test_list(self):
        for i in range(3):
            Comment.objects.create(
                user=self.user,
                post=self.post,
                content='content',
            )
        self.recomment = Comment.objects.create(
            user=self.user,
            parent=Comment.objects.last(),
            content='recomment',
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(f'/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        data = {
            'title': 'testPost',
            'content': 'test Content',
        }

        image = settings.dev.MEDIA_ROOT + '/20/07/08/tree.jpeg'
        test_image = SimpleUploadedFile(
            name='tree.jpeg',
            content=open(image, "rb").read(),
            content_type="image/jpeg"
        )
        data = {
            'title': 'testPost',
            'content': 'test Content',
            'image': test_image,
            'user': self.user.id
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(f'/users/{self.user.id}/posts', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        url = self.url + f'/{self.post.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.user.email, response.data['user']['email'])
        self.assertEqual(self.post.title, response.data['title'])

    def test_update(self):
        url = self.url + f'/{self.post.id}'
        data = {
            'title': 'update Title',
            'content': 'update content',
        }
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.id, response.data['id'])
        self.assertEqual(data['title'], response.data['title'])
        self.assertEqual(data['content'], response.data['content'])

    def test_destroy(self):
        url = self.url + f'/{self.post.id}'
        self.client.force_authenticate(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='testUser@test.com',
            password='1111',
        )
        self.post = Post.objects.create(
            title='test Post title',
            content='test Content title',
            user=self.user
        )
        for i in range(3):
            self.comment = Comment.objects.create(
                content=f'test Content {i}',
                post=self.post,
                user=self.user
            )
        self.recomment = Comment.objects.create(
            content='test Content',
            post=self.post,
            user=self.user,
            parent=self.comment
        )
        self.url = f'/users/{self.user.id}/posts/{self.post.id}/comments'
        self.url_detail = self.url + f'/{self.comment.id}'

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in response.data:
            print(i['content'])
            print(i['id'])

    def test_create(self):
        """
        댓글 작성
        - parent와 post는 공존 할 수 없다. ( comment Serializers 에 의해)
        - parent 만 오는 주소와 /comment/<comment:pk>
        - post 만 오는 주소를 /posts/<post:pk>
        - 구분을 지어야 한다.
        - 둘 다 통합 처리하면 클라이언트에서 알아보기 힘듬
        """

        # 게시글의 댓글을 생성
        self.client.force_authenticate(self.user)
        data = {
            'content': 'test create content',
            'user': self.user.id,
        }
        url = f'/posts/{self.post.id}/comments'
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # 게시글 댓글에 댓글을 생성.
        url = f'/comments/{self.comment.id}/reply'

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        data = {
            'content': 'update content'
        }
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], data['content'])
        self.assertEqual(response.data['id'], self.comment.id)

    def test_destroy(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostLikeTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='testUser@test.com',
            password='1111'
        )
        self.post = Post.objects.create(
            title='test Post',
            content='test content',
            user=self.user,

        )
        self.post2 = Post.objects.create(
            title='test Post',
            content='test content',
            user=self.user,

        )
        self.url = f'/users/{self.user.id}/posts/{self.post2.id}/like'

    def test_like_toggle(self):
        # 좋아요가 눌리지 않은 경우 - 생성 요청
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url + f'/toggle')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['post'], self.post2.pk)
        self.assertEqual(response.data['user'], self.user.pk)

        # 좋아요가 눌린 경우 - 삭제 요청
        like, __ = PostLike.objects.get_or_create(
            post=self.post2,
            user=self.user
        )
        response = self.client.post(self.url + f'/toggle')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentLikeTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='testCommentUser@test.com',
            password='1111'
        )
        self.post = Post.objects.create(
            title='test Post',
            content='test content',
            user=self.user,

        )
        self.comment = Comment.objects.create(
            content='test content',
            post=self.post,
            user=self.user,
        )
        self.comment2 = Comment.objects.create(
            content='test content',
            post=self.post,
            user=self.user,
        )
        self.url = f'/posts/{self.post.pk}/comments/{self.comment2.pk}/like/toggle'

    def test_like_toggle(self):
        # 좋아요가 눌리지 않은 경우 - 생성 요청
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url)
        c = Comment.objects.get(pk=2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], self.comment2.pk)
        self.assertEqual(response.data['user'], self.user.pk)

        # 좋아요가 눌린 경우 - 삭제 요청
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
