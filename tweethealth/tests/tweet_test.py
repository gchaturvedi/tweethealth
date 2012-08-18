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

class TweetTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post_tweet_empty(self):
        request = self.factory.get('/twitter/post-tweet/')
       
        # Test no keys being set
        request.session = { }
        response = views.post_tweet(request)
        self.assertEqual(response.get('Location'),'/')

    def test_post_tweet_http_error(self):
        request = self.factory.get('/twitter/post-tweet/')
        
        # Fill in mock session data to get function to attempt talking to Twitter's API
        request.session = {'twitter_info':{ 'oauth_token' : '22452978-i85AzdfGeHh5s5mbAVcV2EpnC0jz02TxOcC0ZZN6J',
                                            'oauth_token_secret' : 'Zdlk4CkrLpMmDDBGsxWjhWSpqgLQEpIegWREB5NOMqw'},
                                            'health_rating' : '75'}
        response = views.post_tweet(request)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        json_vals = json.loads(response.content)
        self.assertEqual(json_vals['tweet_error'], 1)
        self.assertEqual(json_vals['latest_tweet'], 'Error posting tweet')

