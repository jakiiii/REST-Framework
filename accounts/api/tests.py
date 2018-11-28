from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


# Create your tests here.
class UserTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='jaki', email='jaki@jqurity.com')
        user.set_password('password123')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username='jaki')
        self.assertEqual(qs.count(), 1)

    def test_register_user_api_fail(self):
        url = api_reverse('api-register')
        data = {
            'username': 'sad',
            'email': 'me.sad@khan.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password2'][0], 'This field is required.')

    def test_register_user_api(self):
        url = api_reverse('api-register')
        data = {
            'username': 'sad',
            'email': 'me.sad@khan.com',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token_len = len(response.data.get('token', 0))
        self.assertGreater(token_len, 0)

    def test_login_user_api_fail(self):
        url = api_reverse('api-login')
        data = {
            'username': 'sad',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        token = response.data.get('token', 0)
        token_len = 0
        if token != 0:
            token_len = len(token)
        self.assertEqual(token_len, 0)

    def test_login_user_api(self):
        url = api_reverse('api-login')
        data = {
            'username': 'jaki',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', 0)
        token_len = 0
        if token != 0:
            token_len = len(token)
        self.assertGreater(token_len, 0)

    def test_token_login_api(self):
        url = api_reverse('api-login')
        data = {
            'username': 'jaki',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', None)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_token_register_api(self):
        url = api_reverse('api-login')
        data = {
            'username': 'jaki',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', None)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

        url2 = api_reverse('api-register')
        data2 = {
            'username': 'sad',
            'email': 'me.sad@khan.com',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(url2, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
