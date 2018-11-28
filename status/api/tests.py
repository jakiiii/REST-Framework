import os
import shutil
import tempfile
import pathlib
from PIL import Image

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework.test import APITestCase

from status.models import Status

User = get_user_model()


# Create your tests here.
class StatusAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='j_user', email='jaki@jqurity.com')
        user.set_password('password123')
        user.save()

        status_obj = Status.objects.create(user=user, content='Test Content')

    def test_statuses(self):
        self.assertEqual(Status.objects.count(), 1)

    def status_user_token(self):
        auth_url = api_reverse('api-login')
        auth_data = {
            'username': 'j_user',
            'password': 'password123'
        }
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data.get('token', 0)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    # def test_status_create(self):
    #     self.status_user_token()
    #     url = api_reverse('api-status-list')
    #     data = {
    #         'content': 'Some random content for test'
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Status.objects.all().count(), 2)

    def create_items(self):
        self.status_user_token()
        url = api_reverse('api-status-list')
        data = {
            'content': 'Some random content for test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.all().count(), 2)
        return response.data

    def test_status_create(self):
        data = self.create_items()
        data_id = data.get("id")
        rud_url = api_reverse("api-status-detail", kwargs={"id": data_id})
        rud_data = {
            'content': 'new random content for test'
        }
        """
        retrieve method
        """
        get_response = self.client.get(rud_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_status_create_with_image(self):
        self.status_user_token()
        url = api_reverse('api-status-list')
        # (w, h) = (800, 1280)
        # rgb color -> rgb(255, 255, 255)
        image_item = Image.new('RGB', (800, 1280), (255, 124, 174))
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_item.save(temp_file, format='JPEG')
        with open(temp_file.name, 'rb') as file_obj:
            data = {
                'content': 'Some random content for test',
                'image': file_obj
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Status.objects.all().count(), 2)

        # can't delete delete test image file
        # temp_img = os.path.join(settings.MEDIA_ROOT, 'static-server', 'media-root' 'status')
        # if os.path.exists(temp_img):
        #     os.unlink(temp_img)
        #     pathlib.Path.unlink(temp_img)
        #     shutil.rmtree(temp_img)

    def test_status_create_with_image_without_content(self):
        self.status_user_token()
        url = api_reverse('api-status-list')
        image_item = Image.new('RGB', (800, 1280), (255, 124, 174))
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_item.save(temp_file, format='JPEG')
        with open(temp_file.name, 'rb') as file_obj:
            data = {
                'content': '',
                'image': file_obj
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Status.objects.all().count(), 2)

        # can't delete delete test image file
        # temp_img = os.path.join(settings.MEDIA_ROOT, 'static-server', 'media-root' 'status')
        # if os.path.exists(temp_img):
        #     shutil.rmtree(temp_img)

    def test_status_create_empty_data(self):
        self.status_user_token()
        url = api_reverse('api-status-list')
        image_item = Image.new('RGB', (800, 1280), (255, 124, 174))
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_item.save(temp_file, format='JPEG')
        with open(temp_file.name, 'rb') as file_obj:
            data = {
                'content': None,
                'image': None
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # can't delete delete test image file
        # temp_img = os.path.join(settings.MEDIA_ROOT, 'static-server', 'media-root' 'status')
        # if os.path.exists(temp_img):
        #     shutil.rmtree(temp_img)

    def test_status_update(self):
        data = self.create_items()

        data_id = data.get("id")
        rud_url = api_reverse("api-status-detail", kwargs={"id": data_id})
        rud_data = {
            'content': 'new random content for test'
        }
        put_response = self.client.put(rud_url, rud_data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        rud_response_data = put_response.data
        self.assertEqual(rud_response_data['content'], rud_data['content'])

    def test_status_delete(self):
        data = self.create_items()

        data_id = data.get("id")
        rud_url = api_reverse("api-status-detail", kwargs={"id": data_id})
        rud_data = {
            'content': 'new random content for test'
        }

        delete_response = self.client.delete(rud_url, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        """
        Not Found
        """
        delete_response = self.client.delete(rud_url, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_create_no_token(self):
        url = api_reverse('api-status-list')
        data = {
            'content': 'Some random content for test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
