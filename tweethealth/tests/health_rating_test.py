"""
This file contains tests for the update_health_rating view function.
It uses the mock library to mock out some of the messaging that happens
with Twitter, instead of interacting it Twitter it uses mock or fake data.
"""
import json
import mock

from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from twython import Twython, TwythonError, TwythonRateLimitError

from tweethealth import views

class UpdateHealthRatingTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        
    def fake_twitter_zero_health(request):
        return 0, 'Fake tweet msg'

    def fake_twitter_twenty_five_health(request):
        return 25, 'Fake tweet msg'

    def fake_twitter_seventy_five_health(request):
        return 75, 'Fake tweet msg'

    def fake_twitter_hundred_health(request):
        return 100, 'Fake tweet msg'
        
    @mock.patch("tweethealth.views._get_twitter_data", fake_twitter_zero_health)
    def test_twitter_zero_five_context(self):
        response = self.client.post('/twitter/update-timeline/')
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.context['health_rating'], 0)
        self.assertEqual(response.context['health_msg'], 'Do you like not use Twitter? Not cool.')
    
    @mock.patch("tweethealth.views._get_twitter_data", fake_twitter_twenty_five_health)
    def test_twitter_twenty_five_context(self):
        response = self.client.post('/twitter/update-timeline/')
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.context['health_rating'], 25)
        self.assertEqual(response.context['health_msg'], 'Meh...you could do better..hit the gym buddy.')
    
    @mock.patch("tweethealth.views._get_twitter_data", fake_twitter_seventy_five_health)
    def test_twitter_seventy_five_context(self):
        response = self.client.post('/twitter/update-timeline/')
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.context['health_rating'], 75)
        self.assertEqual(response.context['health_msg'], 'You\'re okay, but not super healthy.')

    @mock.patch("tweethealth.views._get_twitter_data", fake_twitter_hundred_health)
    def test_twitter_hundred_context(self):
        response = self.client.post('/twitter/update-timeline/')
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.context['health_rating'], 100)
        self.assertEqual(response.context['health_msg'], 'Good for you...you work out and eat well.')

    def fake_twython_401_error(request):
        raise TwythonError(msg='401 error',error_code=401)

    def fake_twython_403_error(request):
        raise TwythonError(msg='403 error',error_code=401)

    def fake_twython_other_error(request):
        raise TwythonError(msg='Other error',error_code=406)

    @mock.patch("tweethealth.views._get_twitter_data", fake_twython_401_error)
    def test_twitter_hundred_context(self):
        response = self.client.post('/twitter/update-timeline/')
        json_vals = json.loads(response.content)
        self.assertEqual(json_vals['auth_error'], 1)
        self.assertEqual(json_vals['twitter_error'], 1)

    @mock.patch("tweethealth.views._get_twitter_data", fake_twython_403_error)
    def test_twitter_hundred_context(self):
        response = self.client.post('/twitter/update-timeline/')
        json_vals = json.loads(response.content)
        self.assertEqual(json_vals['rate_error'], 1)
        self.assertEqual(json_vals['twitter_error'], 1)

    @mock.patch("tweethealth.views._get_twitter_data", fake_twython_other_error)
    def test_twitter_hundred_context(self):
        response = self.client.post('/twitter/update-timeline/')
        json_vals = json.loads(response.content)
        self.assertEqual(json_vals['twitter_error'], 1)
