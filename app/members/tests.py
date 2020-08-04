from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from members.models import Profile, Relations, RecentlyUser
from posts.models import Post, Comment

User = get_user_model()


class UserTest(APITestCase):
    url = '/users'

    # def setUp(self) -> None:
        # self.user = User(email='jeonyh0924@naver.com', password='1111')
        # self.user.set_password(self.user.password)
        # self.user.save()
        # self.user2 = User.objects.create_user(email='test2@email', password='1111')

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        data = {
            'email': 'jeonyh0924@naver.com',
            'password': '1111',
            'username': 'testUser'
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.data
        self.assertEqual(response_data['email'], data['email'])

        # 유저 생성 시 프로필이 올바르게 생성이 되었는지
        user = User.objects.get(email=data['email'])
        self.assertTrue(user.profile)

    def test_retrieve(self):
        url = f'/users/{self.user.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, response.data['email'])
        self.assertEqual(self.user.id, response.data['id'])

    def test_partial_update(self):
        data = {
            'password': '1111',
        }
        url = f'/users/{self.user.id}'
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['id'], self.user.id)

    def test_destroy(self):
        url = self.url + f'/{self.user.id}'
        self.client.force_authenticate(self.user)
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

    def test_page(self):
        self_user_post = Post.objects.create(user=self.user, title='self_user_title', content='self_user')
        Relations.objects.create(from_user=self.user, to_user=self.user2, related_type='f')
        post = Post.objects.create(user=self.user2, title='title', content='content')
        Comment.objects.create(post=post, user=self.user2, content='content')
        user = User.objects.create_user(email='BlockUser@test.com', password='1111')

        Relations.objects.create(from_user=self.user, to_user=user, related_type='b')
        post = Post.objects.create(user=user, title='title2', content='content2')
        Comment.objects.create(post=post, user=user, content='comment')

        self.client.force_authenticate(self.user)
        response = self.client.get('/users/page')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_username(self):
        """
        :return:        특정 유저 이름을 검색하면 유저에 대한 데이터 리턴
        """
        self.client.force_authenticate(self.user)
        User.objects.create_user('testUser@user.com', '1111')
        User.objects.create_user('testFilterUser@user.com', '1111')

        response = self.client.get('/users?username=test')
        filter_data = User.objects.filter(profile__username__startswith='test')
        for res_data, query_data in zip(response.data, filter_data):
            self.assertEqual(res_data['id'], query_data.id)
            self.assertEqual(res_data['email'], query_data.email)
        response = self.client.get('/users?username=testUser')
        filter_data = User.objects.filter(profile__username__startswith='testUser')
        for res_data, query_data in zip(response.data, filter_data):
            self.assertEqual(res_data['id'], query_data.id)
            self.assertEqual(res_data['email'], query_data.email)

    def test_myPost(self):
        self.client.force_authenticate(self.user)
        post = Post.objects.create(
            title='User Post',
            content='content',
            user=self.user
        )
        co = Comment.objects.create(post=post, user=self.user, content='comment')
        co2 = Comment.objects.create(parent=co, user=self.user, content='comment2')

        response = self.client.get('/users/myProfile')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_retrieve(self):
        # 특정 프로필에 조회를 할 경우
        self.client.force_authenticate(self.user)
        url = self.url + f'/{self.user.id}/profile/{self.user.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update(self):
        data = {
            'username': 'updateUser',
            'introduce': 'update introduce'
        }
        response = self.client.patch(f'/users/{self.user.id}/profile/{self.user.profile.id}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['introduce'], data['introduce'])

    def test_change_password(self):
        url = self.url + f'/{self.user.id}/change-password'
        self.client.force_authenticate(self.user)
        # 비밀번호가 맞는 경우.
        data = {
            "old_password": '1111',
            "new_password": '2222',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 비밀번호가 틀린 경우
        data = {
            "old_password": '11111',
            "new_password": '2222',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow_user(self):
        user3 = User.objects.create_user(
            email='u3@u3.com',
            password='1111'
        )

        Relations.objects.create(from_user=self.user, to_user=self.user2, related_type='f')
        Relations.objects.create(from_user=self.user, to_user=user3, related_type='f')
        self.client.force_authenticate(self.user)
        response = self.client.get('/users/follow')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follower_user(self):
        user3 = User.objects.create_user(
            email='user3@test.com',
            password='1111'
        )
        Relations.objects.create(from_user=user3, to_user=self.user, related_type='f')
        self.client.force_authenticate(self.user)
        response = self.client.get('/users/follower/')

    def test_make_relation(self):
        self.client.force_authenticate(self.user)
        data = {
            'related_type': 'f',
        }
        response = self.client.post(f'/users/{self.user2.id}/relation', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 동일한 relation을 생생 시키려 한다면
        response = self.client.post(f'/users/{self.user2.id}/relation', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 동일한 유저의 relation 생성 불가.
        data = {
            'from_user': self.user.id,
            'to_user': self.user.id,
            'related_type': 'f',
        }
        response = self.client.post(f'/users/{self.user.id}/relation', data=data)


class RelationTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='test@test.com',
            password='1111',
        )
        data = {
            'email': 'testUser@test.com',
            'password': '1111',
            'username': 'username'
        }
        response = self.client.post('/users', data=data)
        self.r = Relations.objects.create(from_user=User.objects.first(),
                                          to_user=User.objects.get(pk=2),
                                          related_type='f'
                                          )

    def test_update(self):
        self.client.force_authenticate(self.user)
        user2 = User.objects.create_user(
            email='testUser2@test.com',
            password='1111'
        )
        data = {
            'related_type': 'f'
        }
        response = self.client.post(f'/users/{user2.id}/relation', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        profile_response = self.client.get(f'/users/{self.user.pk}/profile/{self.user.profile.pk}')
        r = Relations.objects.last()
        response = self.client.patch(f'/relation/{self.r.pk}', {"related_type": "b"})
        # count 확인 로직
        profile_response = self.client.get(f'/users/{self.user.pk}/profile/{self.user.profile.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RecentlyTest(APITestCase):
    def setUp(self) -> None:
        self.from_user = User.objects.create_user('from_user@test.com', '1111')
        self.to_user = User.objects.create_user('to_user@test.com', '1111')
        self.other_user = User.objects.create_user('otherUser@test.com', '1111')
        r1 = RecentlyUser.objects.create(from_user=self.from_user, to_user=self.to_user)
        r2 = RecentlyUser.objects.create(from_user=self.from_user, to_user=self.other_user)

    def test_list(self):
        """
        최근에 검색한 유저 프로필 저옵가 제일 위에 오도록
        """
        self.client.force_authenticate(self.from_user)
        response = self.client.get(f'/users/{self.from_user.id}/recently')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        limit_user = User.objects.create_user('limit@limit.com', '1111')
        self.client.force_authenticate(self.from_user)
        # data = {
        #     'from_user': self.from_user.id,
        #     'to_user': self.to_user.id,
        # }
        print(User.objects.filter(recently_to_user__from_user=self.from_user.id))
        # 올바른 recently 생성
        response = self.client.post(f'/users/{self.to_user.id}/recently')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(User.objects.filter(recently_to_user__from_user=self.from_user.id))
        response = self.client.post(f'/users/{self.other_user.id}/recently')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(User.objects.filter(recently_to_user__from_user=self.from_user.id))
        # 3개 이상의 최근 유저 검색 리스트가 있다면, 가장 오래된 검색 기록을 삭제한다.
        response = self.client.post(f'/users/{limit_user.id}/recently')
        print(User.objects.filter(recently_to_user__from_user=self.from_user.id))

        # 존재하지 않는 to_user 생성 시 , 404 에러 발생
        response = self.client.post(f'/users/100/recently')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.fail()
