"""
Just to force 100% coverage
"""
from django.test import SimpleTestCase

from vanityurls.models import Category


class ModelUnitTest(SimpleTestCase):

    def test_fields(self):
        category = Category()
        category.name = 'My Test Category'
        self.assertEqual(str(category), category.name)
