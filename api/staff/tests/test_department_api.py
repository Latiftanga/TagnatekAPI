from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Role

DEPARTMENT_URL = reverse('staff:department-list')


class PublicDepartmentAPITest(TestCase):
    '''Test public API for staff Department'''

    def setUp(self):
        self.client = APIClient()

    def test_that_unauthenticated(self):
        '''Test that unauthenticated user can't access dept list'''

        res = self.client.get(DEPARTMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDepartmentAPITest(TestCase):
    '''Test private Staff Departments'''

    def setUp(self):

        admin_role = Role.objects.create(name='admin')
        teacher_role = Role.objects.create(name='teacher')

        self.admin = get_user_model().objects.create_user(
            email='admin@eg.com',
            password='admin@pass',
            role=admin_role
            )
        self.teacher = self.teacher = get_user_model().objects.create_user(
            email='teacher@eg.com',
            password='teacher@pass',
            role=teacher_role
            )
        self.teacher_client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(self.admin)
        self.teacher_client.force_authenticate(self.teacher)

    def test_non_admin_user_dept_list(self):
        '''test that a non admin can't access department list'''

        res = self.teacher_client.get(DEPARTMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
