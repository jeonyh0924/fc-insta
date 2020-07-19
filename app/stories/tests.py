from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase

User = get_user_model()


class StoryTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='testUser@test.com', password='1111')

    # def test_list(self):
    #     self.fail()

    def test_create(self):
        self.client.force_authenticate(self.user)
        data = {
            'content': 'content',
        }
        response = self.client.post(f'/users/{self.user.pk}/story', data=data)
        self.fail()
