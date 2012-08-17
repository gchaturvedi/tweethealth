import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from twython import Twython, TwythonError

# Constants
FIRST_IDX = 0

# Public Methods
def homepage(request):
    """
    This method is reponsible for displaying the homepage for
    TweetHealth.
    """
    # set the default context dictionary and template to be displayed
    context = { }
    template = 'homepage.html'

    # check if website visitor has already given access to their twitter account
    if 'twitter_info' in request.session:
        context = _twitter_display_context(request)
        template = 'twitter_homepage.html'

    return render_to_response(
            template,
            context,
            context_instance=RequestContext(request))

def update_health_rating(request):
    try:
        health_rating, latest_tweet = _get_twitter_data(request)
        json_return_val = { 'health_rating' : health_rating, 
                            'latest_tweet' : latest_tweet,
                            'twitter_error': 0 }
    except TwythonError:
        json_return_val = { 'twitter_error': 1 }
            
    return HttpResponse(json.dumps(json_return_val), mimetype="application/json")
    
# Private Methods
def _twitter_display_context(request):
    """
    This method 
    """
    context = { }
    
    try:
        twitter = Twython(
            twitter_token = settings.TWITTER_KEY,
            twitter_secret = settings.TWITTER_SECRET,
            oauth_token = request.session['twitter_info']['oauth_token'],
            oauth_token_secret = request.session['twitter_info']['oauth_token_secret'],
        )
        
        context.update({'twitter_username' : request.session['twitter_info']['screen_name']})
    
    except KeyError:
        return HttpResponseRedirect(settings.AUTHORIZE_COMPLETE_URL)
                    
    return context

def _get_twitter_data(request):
    try:
        twitter = Twython(
            twitter_token = settings.TWITTER_KEY,
            twitter_secret = settings.TWITTER_SECRET,
            oauth_token = request.session['twitter_info']['oauth_token'],
            oauth_token_secret = request.session['twitter_info']['oauth_token_secret'],
        )
    
    except KeyError:
        return HttpResponseRedirect(settings.AUTHORIZE_COMPLETE_URL)
        
    user_timeline = twitter.getUserTimeline()
    
    if user_timeline:
        latest_tweet = user_timeline[FIRST_IDX]
    else:
        latest_tweet = ''
        
    new_health_rating = _determine_health_rating(
        user_timeline=user_timeline,
        home_timeline=twitter.getHomeTimeline()
    )
    
    return new_health_rating, latest_tweet
    
def _determine_health_rating(user_timeline=None, home_timeline=None):
    if user_timeline is None and home_timeline is None:
        return 5
    else:
        return 0
        