from django.test import TestCase
from django.contrib.auth import get_user_model

from status.models import Status

User = get_user_model()


# Create your tests here.
class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='jaki', email='jaki@jqurity.com')
        user.set_password('password123')
        user.save()

    def test_creating_status(self):
        user = User.objects.get(username='jaki')
        obj = Status.objects.create(user=user, content='random test content. ')
        self.assertEqual(obj.id, 1)
        qs = Status.objects.all()
        self.assertEqual(qs.count(), 1)
