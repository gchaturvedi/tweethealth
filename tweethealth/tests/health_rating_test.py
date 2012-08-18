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

from twython import Twython, TwythonError, TwythonRateLimitError

from tweethealth import views

class UpdateHealthRatingTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        
    def fake_twitter_zero_health(request):
        return 0, 'This dudes got no health'

    def fake_twitter_twenty_five_health(request):
        return 25, 'They will get by'

    def fake_twitter_seventy_five_health(request):
        return 75, 'Hooba hooba fake twitter test'

    def fake_twitter_hundred_health(request):
        return 100, 'Yeah he is healthy'

    @mock.patch("tweethealth.views._get_twitter_data", fake_twitter_seventy_five_health)
    def test_twitter_health_rating(self):
        request = self.factory.get('/twitter/update-timeline/')
        request.session = { }
        response = views.update_health_rating(request)
        
    @mock.patch("tweethealth.views._get_twitter_data", fake_twitter_zero_health)
    def test_twitter_zero_five_context(self):
        response = self.client.post('/twitter/update-timeline/')
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.context['health_rating'], 0)
        self.assertEqual(response.context['latest_tweet'], 'This dudes got no health')
        self.assertEqual(response.context['health_msg'], 'Do you like not use Twitter? Not cool.')
    
    @mock.patch("tweethealth.views._get_twitter_data", fake_twitter_twenty_five_health)
    def test_twitter_twenty_five_context(self):
        response = self.client.post('/twitter/update-timeline/')
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.context['health_rating'], 25)
        self.assertEqual(response.context['latest_tweet'], 'They will get by')
        self.assertEqual(response.context['health_msg'], 'Meh...you could do better..hit the gym buddy.')
    
    @mock.patch("tweethealth.views._get_twitter_data", fake_twitter_seventy_five_health)
    def test_twitter_seventy_five_context(self):
        response = self.client.post('/twitter/update-timeline/')
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.context['health_rating'], 75)
        self.assertEqual(response.context['latest_tweet'], 'Hooba hooba fake twitter test')
        self.assertEqual(response.context['health_msg'], 'You\'re okay, but not super healthy.')

    @mock.patch("tweethealth.views._get_twitter_data", fake_twitter_hundred_health)
    def test_twitter_hundred_context(self):
        response = self.client.post('/twitter/update-timeline/')
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.context['health_rating'], 100)
        self.assertEqual(response.context['latest_tweet'], 'Yeah he is healthy')
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
