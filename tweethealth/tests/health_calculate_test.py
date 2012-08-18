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

class HealthCalculateTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        
