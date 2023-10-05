from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


# Create your tests here.
class UserTestCase(APITestCase):
    def setUp(self):

        self.url = '/users/'

        self.phone = {'phone': '70000000000'}
        self.wrong_phone = {'phone': '7000000000q'}

        self.phone_1 = {'phone': '70000000001'}
        self.user_1 = User.objects.create(
            phone=self.phone_1['phone'],
            personal_invitation_code='qwe111')
        self.user_1.set_password('1111')
        self.user_1.save()

        self.phone_2 = {'phone': '7000000002'}
        self.user_2 = User.objects.create(
            phone=self.phone_2['phone'],
            personal_invitation_code='qwe222')
        self.user_2.set_password('2222')
        self.user_2.save()

    def test_post_login_api_view(self):

        response = self.client.post(path=f'{self.url}login/', data=self.phone)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()

        self.assertEqual(
            response['message'], 'Код отправлен на телефон(почту)',
        )

    def test_post_negative_post_login_api_view(self):

        response = self.client.post(
            path=f'{self.url}login/', data=self.wrong_phone)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = response.json()

        self.assertEqual(
            response['message'],
            'Неверный формат телефона, должен быть в формате 7 800 800 80 80',
        )

    def test_post_verify_api_view(self):

        data = {
            'phone': self.user_1.phone,
            'password': '1111',
        }

        response = self.client.post(path=f'{self.url}verify/', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()

        self.assertTrue(isinstance(response.get('access_token'), str))
        self.assertTrue(isinstance(response.get('refresh_token'), str))
        self.assertTrue(len(response.get('access_token')) > 0)
        self.assertTrue(len(response.get('refresh_token')) > 0)

    def test_post_wrong_pass_verify_api_view(self):

        data = {
            'phone': self.user_1.phone,
            'password': '1110',
        }

        response = self.client.post(path=f'{self.url}verify/', data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = response.json()

        self.assertEqual(response.get('message'), 'Неверный пароль')

    def test_post_wrong_phone_verify_api_view(self):

        data = {
            'phone': self.wrong_phone['phone'],
            'password': '1111',
        }

        response = self.client.post(path=f'{self.url}verify/', data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = response.json()

        self.assertEqual(response.get('message'),
                         'Такого пользователя не существует')

    def test_post_refresh_token_api_view(self):

        data = {
            'phone': self.user_1.phone,
            'password': '1111',
        }

        response = self.client.post(path=f'{self.url}verify/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()

        data = {
            'refresh_token': response.get('refresh_token'),
        }
        response = self.client.post(path=f'{self.url}refresh/', data=data)
        response = response.json()

        self.assertTrue(isinstance(response.get('access_token'), str))
        self.assertTrue(len(response.get('access_token')) > 0)

    def test_post_refresh_wrong_token_api_view(self):

        data = {
            'refresh_token': 'UzNDJkNWZkM2U1IiX9pZCI6N30',
        }
        response = self.client.post(path=f'{self.url}refresh/', data=data)
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)
        response = response.json()

        self.assertEqual(response['message'], 'Неверный токен')

    def test_get_profile_retrieve_api_view(self):

        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(
            path=f'{self.url}retrieve/{self.user_1.phone}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()

        self.assertEqual(response.get('email'), self.user_1.email)
        self.assertEqual(response.get('phone'), self.user_1.phone)
        self.assertEqual(response.get('first_name'), self.user_1.first_name)
        self.assertEqual(response.get('last_name'), self.user_1.last_name)
        self.assertEqual(response.get('personal_invitation_code'),
                         self.user_1.personal_invitation_code)
        self.assertEqual(response.get('someone_invite_code'),
                         self.user_1.someone_invite_code)
        self.assertEqual(response.get('invited_users'), [])

    def test_get_wrong_profile_retrieve_api_view(self):

        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(
            path=f'{self.url}retrieve/{self.wrong_phone["phone"]}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = response.json()

        self.assertEqual(response.get('detail'), 'Not found.')

    def test_get_not_current_profile_retrieve_api_view(self):

        self.client.force_authenticate(user=self.user_2)

        response = self.client.get(
            path=f'{self.url}retrieve/{self.user_1.phone}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = response.json()

        self.assertEqual(response.get('detail'),
                         'You do not have permission to perform this action.')

    def test_put_profile_update_api_view(self):

        self.client.force_authenticate(user=self.user_1)
        data = {
            'email': 'qwe@qwe.com',
            'first_name': 'qwe',
            'last_name': 'qwe',
            'someone_invite_code': 'qwe222',
        }

        response = self.client.put(
            path=f'{self.url}update/{self.user_1.phone}/',
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response.get('email'), 'qwe@qwe.com')
        self.assertEqual(response.get('first_name'), 'qwe')
        self.assertEqual(response.get('last_name'), 'qwe')
        self.assertEqual(response.get('someone_invite_code'), 'qwe222')

    def test_put_non_exist_code_profile_update_api_view(self):
        
        self.client.force_authenticate(user=self.user_1)
        data = {
            'email': 'qwe@qwe.com',
            'first_name': 'qwe',
            'last_name': 'qwe',
            'someone_invite_code': 'qweqwe',
        }

        response = self.client.put(
            path=f'{self.url}update/{self.user_1.phone}/',
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = response.json()
        
        self.assertEqual(response.get('message'), 
                         ['Код приглашения не существует'])
