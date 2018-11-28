from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='jaki', email='jaki@jqurity.com')
        user.set_password('password123')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username='jaki')
        self.assertEqual(qs.count(), 1)
