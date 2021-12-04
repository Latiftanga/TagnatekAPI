from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test creating a user with email is successful'''

        email = 'email@test.com'
        password = 'test@pass.com'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_email_normalize(self):
        '''Test creating a user with email is normalise'''
        email = 'email@TEST.com'
        password = 'test@pass'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''Test creating new user with invalid email'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test@pass')

    def test_create_superuser_successful(self):
        '''Test creating a super user successful'''

        user = get_user_model().objects.create_superuser(
            email='admin@eg.com',
            password='admin@pass'
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
