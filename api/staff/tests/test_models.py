from django.test import TestCase
from staff import models


class ModelTest(TestCase):

    def test_department_str(self):
        '''Test string representation of dept'''

        dept = models.Department.objects.create(
            name='Accounting'
            )

        self.assertEqual(str(dept), dept.name)
