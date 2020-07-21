from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase

from config import settings
from members.models import Relations
from stories.models import Story

User = get_user_model()


class StoryTest(APITestCase):
    def setUp(self) -> None:
        image = settings.dev.MEDIA_ROOT + '/20/07/08/tree.jpeg'
        test_image = SimpleUploadedFile(
            name='tree.jpeg',
            content=open(image, "rb").read(),
            content_type="image/jpeg"
        )
        video = settings.dev.MEDIA_ROOT + '/video/video.mov'
        self.video_data = SimpleUploadedFile(
            name="video.mov",
            content=open(video, 'rb').read(),
            content_type="video/mov"
        )
        self.user = User.objects.create_user(email='testUser@test.com', password='1111')
        self.user2 = User.objects.create_user(email='testUser2@test.com', password='1111')

        self.r1 = Relations.objects.create(from_user=self.user2, to_user=self.user, related_type='f')

        self.story1 = Story.objects.create(user=self.user, content='content', image=test_image)
        self.story2 = Story.objects.create(user=self.user, content='content', image=test_image)

    def test_list(self):
        """
        유저2가 팔로우한 유저1에 대한 게시글 정보
         - 팔로우 하지 않은 유저의 스토리 생성 [0]
         - 팔로우를 하였지만, 24시간이 넘은 스토리를 생성. [0]
        """
        unFollowUser = User.objects.create_user(email='unFUser@user.com', password='1111')
        unFollowStory = Story.objects.create(user=unFollowUser)

        pastStory = Story.objects.create(user=self.user)
        pastStory.created_at -= timedelta(days=2)
        pastStory.save()

        self.client.force_authenticate(self.user2)
        response = self.client.get(f'/users/{self.user2.id}/story')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertTrue(response.data['next'])

        response = self.client.get(f'/users/{self.user2.id}/story/{self.story1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        """
        - 이미지 생성 [0]
        - 동영상 생성 [0]
        """
        self.client.force_authenticate(self.user)
        image = settings.dev.MEDIA_ROOT + '/20/07/08/tree.jpeg'

        image_data = SimpleUploadedFile(
            name='tree.jpeg',
            content=open(image, "rb").read(),
            content_type="image/jpeg"
        )

        data = {
            'content': 'content',
            'image': image_data,
        }
        response = self.client.post(f'/users/{self.user.pk}/story', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['image'])
        self.assertFalse(response.data['video'])

        mov_data = {
            'content': 'content with image file',
            'video': self.video_data
        }
        response = self.client.post(f'/users/{self.user.pk}/story', data=mov_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['video'])
        self.assertFalse(response.data['image'])

    def test_retrieve(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f'/users/{self.user.pk}/story/{self.story1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
