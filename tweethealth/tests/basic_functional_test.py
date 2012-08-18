"""
This file contains all the tests for the TweetHealth app.  The tests
can be run with the test runner by using this command:

python manage.py test

"""
import json
import mock

from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from tweethealth import views

class BasicFunctionalTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_404_page(self):
        """
        Tests that 404 page exists and unrouted URLs are forwarded to it.
        """
        response = self.client.get('/random-page/')
        self.assertEqual(response.status_code,404)

