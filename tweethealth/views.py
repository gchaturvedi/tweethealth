from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from twython import Twython

def homepage(request):
	"""
		This method is reponsible for displaying the homepage for
		TweetHealth.
	"""
	# set the default context dictionary and template to be displayed
	context = { }
	template = 'homepage.html'

	# check if website visitor has already given access to their twitter account
	if 'screen_name' in request.session['twitter_info']:
		context = twitter_display_context(request)
		template = 'twitter_homepage.html'
	
	return render_to_response(
	        template,
	        context,
	        context_instance=RequestContext(request))

def twitter_display_context(request):
	context = { 'twitter_username' : request.session['twitter_info']['screen_name'] }
	return context
	
def twitter_connect(request):
	"""
		This method begins the three legged oAuth handshake between
		TweetHealth and Twitter.
	"""
	twitter = Twython(
		twitter_token = settings.TWITTER_KEY,
		twitter_secret = settings.TWITTER_SECRET,
		callback_url = 'http://localhost:8000/login-confirm/'
	)

	auth_dict = twitter.get_authentication_tokens()

	request.session['request_token'] = auth_dict
	return HttpResponseRedirect(auth_dict['auth_url'])

def twitter_authorized(request, redirect_url=settings.AUTHORIZE_COMPLETE_URL):
	"""
		This method is a callback from Twitter which is triggered after
		the user signs in and allows authorization of their Twitter account.
	"""
	twitter = Twython(
		twitter_token = settings.TWITTER_KEY,
		twitter_secret = settings.TWITTER_SECRET,
		oauth_token = request.session['request_token']['oauth_token'],
		oauth_token_secret = request.session['request_token']['oauth_token_secret'],
	)

	twitter_info = twitter.get_authorized_tokens()
	request.session['twitter_info'] = twitter_info
	return HttpResponseRedirect(redirect_url)
