from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('core:create_user')
TOKEN_URL = reverse('core:token')
ME_URL = reverse('core:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserTestAPI(TestCase):
    '''Test User API Public'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        '''Test creating a user with valid payload successful'''
        payload = {"email": "test@eg.com", "password": "test@pass"}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.filter(email=res.data['email']).first()

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        '''Test creating a user that already exists fails'''
        payload = {"email": "test@eg.com", "password": "test@pass"}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''Testing creating user with less than 5 characters fails'''
        payload = {"email": "test@eg.com", "password": "p"}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
            ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        payload = {'email': 'test@eg.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials"""
        create_user(email='test@eg.com', password='testpass')
        payload = {'email': 'test@eg.com', 'password': 'wrongpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test a token is not created if user does not exist"""
        payload = {'email': 'test@twysolutions.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and password is required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_anauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
