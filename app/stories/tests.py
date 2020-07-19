import io

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from config import settings
from members.models import Relations
from stories.models import Story, StoryImage

User = get_user_model()


class StoryTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='testUser@test.com', password='1111')
        self.user2 = User.objects.create_user(email='testUser2@test.com', password='1111')

        self.r1 = Relations.objects.create(from_user=self.user2, to_user=self.user, related_type='f')

        self.story1 = Story.objects.create(user=self.user, content='content', )
        image = settings.dev.MEDIA_ROOT + '/20/07/08/tree.jpeg'
        test_image = SimpleUploadedFile(
            name='tree.jpeg',
            content=open(image, "rb").read(),
            content_type="image/jpeg"
        )
        StoryImage.objects.create(story=self.story1, image=test_image)

    def test_list(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get(f'/users/{self.user.id}/story')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        self.client.force_authenticate(self.user)
        data = {
            'content': 'content',
        }
        response = self.client.post(f'/users/{self.user.pk}/story', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        image = settings.dev.MEDIA_ROOT + '/20/07/08/tree.jpeg'
        test_image = SimpleUploadedFile(
            name='tree.jpeg',
            content=open(image, "rb").read(),
            content_type="image/jpeg"
        )

        img_data = {
            'content': 'content with image file',
            'image': test_image,
        }
        response = self.client.post(f'/users/{self.user.pk}/story', data=img_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
