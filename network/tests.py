from django.test import TestCase

from .models import User

# Create your tests here.
class UserTestCase(TestCase):

    def setUp(self):

        # Create user
        User.objects.create(username="mazen", first_name="Mazen", last_name="Magdy")


    def test_valid_user(self):
        """ Check first name not equal last name """
        user = User.objects.get(username="mazen")
        self.assertTrue(user.is_valid_user())