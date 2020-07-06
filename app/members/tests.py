from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class UserTest(APITestCase):
    url = '/users/user'

    def setUp(self) -> None:
        self.user = User(email='test@email.com', password='1111')
        self.user.set_password(self.user.password)
        self.user.save()

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        data = {
            'email': 'create@user.com',
            'password': '1111',
            'username': 'testUser'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.data
        self.assertEqual(response_data['email'], data['email'])

    def test_retrieve(self):
        url = self.url + f'/{self.user.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, response.data['email'])
        self.assertEqual(self.user.id, response.data['id'])

    def test_partial_update(self):
        data = {
            'password': '1111',
        }
        url = self.url + f'/{self.user.id}'
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['id'], self.user.id)

    def test_destroy(self):
        url = self.url + f'/{self.user.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_login(self):
        # 회원 가입이 올바른 경우
        data = {
            'email': self.user.email,
            'password': '1111'
        }
        url = self.url + f'/login'
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['token'])

        # 올바르지 않은 유저가 접근하는 경우
        data = {
            'email': self.user.email,
            'password': "11111"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 기존에 토큰을 생성한 유저일 경우
        data = {
            'email': self.user.email,
            'password': '1111'
        }
        url = self.url + f'/login'
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])

    def test_logout(self):
        self.client.force_authenticate(self.user)
        token = Token.objects.create(user=self.user)
        url = self.url + '/logout'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(token.key)

        self.assertEqual(Token.objects.filter(user=self.user).first(), None)

