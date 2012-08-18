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

class OAuthTwitterTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_twitter_connect(self):
        """
        Tests that the redirect to Twitter is being conducted properly at the /login/ url.
        """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('https://api.twitter.com/oauth/authenticate?oauth_token=' in response.get('Location'))
        
    def test_twitter_authorized_redirect(self):
        """
        Tests response redirect from Twitter back to TweetHealth 
        """
        response = self.client.get('/login-confirm/')
        self.assertEqual(response.status_code, 302)        
                

