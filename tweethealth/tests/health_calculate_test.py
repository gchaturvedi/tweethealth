"""
This file contains tests that ensure that the health rating is
calculated properly on Twitter (mock) data.  It also ensures that
the function that gets Twitter data is behaving properly.
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
