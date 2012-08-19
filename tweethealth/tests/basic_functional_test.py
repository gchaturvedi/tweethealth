"""
These are basic functional unit tests site-wide.  They
test things such as 404s being displayed, general homepage checks.
"""
from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from tweethealth import views

class BasicFunctionalTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        
    def test_homepage_no_twitter(self):
        """
        Tests that the homepage displays proper content and a button to
        login via Twitter if person has not yet logged in via Twitter.
        """
        response = self.client.get('/')
        self.assertTrue('Login' in response.content)
        self.assertEqual(response.templates[0].name, 'homepage.html')

    def test_homepage_with_twitter(self):
        """
        Tests that the homepage displays twitter related content by
        mocking out a user returning to the homepage after Twitter
        sign in.
        """
        request = self.factory.get('/')
        request.session = {'twitter_info':{ 'oauth_token' : '22452978-i85AzdfGeHh5s5mbAVcV2EpnC0jz02TxOcC0ZZN6J',
                                            'oauth_token_secret' : 'Zdlk4CkrLpMmDDBGsxWjhWSpqgLQEpIegWREB5NOMqw'}}
        response = views.homepage(request)
        self.assertEqual(response.status_code,200)
        self.assertTrue('Your score' in response.content)   
        
    def test_about_page(self):
        """
        Tests that the about homepage is displayed.
        """
        response = self.client.get('/about/')
        self.assertEqual(response.templates[0].name, 'about.html')
    
    def test_404_page(self):
        """
        Tests that 404 page exists and unrouted URLs are forwarded to it.
        """
        response = self.client.get('/random-page/')
        self.assertEqual(response.status_code,404)
