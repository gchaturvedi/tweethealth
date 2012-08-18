"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class OAuthTwitterTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_twitter_connect(self):
        """
        Tests that the redirect to Twitter is being conducted properly.
        """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('https://api.twitter.com/oauth/authenticate?' in response.items()[2][1])
