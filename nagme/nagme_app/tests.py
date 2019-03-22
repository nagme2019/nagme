from django.test import TestCase
from myapp.models import *

class categoryTests(TestCase):
    def setup(self):
        Category.objects.create(name="test",)
        Category.objects.create(name="slug test")

    def test_category_slug(self):
        """Categories are correctly identified and slugs are generated correctly"""
        test = Category.objects.get(name="test")
        slugtest = Category.objects.get(name="slug test")
        self.assertEquals(test.slug, 'test')
        self.assertEqual(slugtest.slug, 'slug_test')

class nagTests(TestCase):
    def setup(self):
    Nag.objects.create(text="testing")

    def test_something(self):

