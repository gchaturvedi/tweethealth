import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from twython import Twython, TwythonError, TwythonRateLimitError

# Constants

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

def about(request):
    """
    This method is reponsible for displaying the about page for
    TweetHealth.
    """
    return render_to_response(
            'about.html',
            context_instance=RequestContext(request))

def update_health_rating(request):
    """
    This is a view function that is a callback from a POST request
    sent from the user's browser.  This will be triggered periodically.
    """
    try:
        health_rating, latest_tweet = _get_twitter_data(request)
        
        # determine string to display based on health
        if health_rating == 0:
            health_msg = 'Do you like not use Twitter? Not cool.'
        elif health_rating > 0 and health_rating <= 50:
            health_msg = 'Meh...you could do better..hit the gym buddy.'
        elif health_rating > 50 and health_rating <= 80:
            health_msg = 'You\'re okay, but not super healthy.'
        else:
            health_msg = 'Good for you...you work out and eat well.'
            
        # twitter_error indicates an API error / Rate Limit being hit
        json_return_val = { 'health_rating' : health_rating, 
                            'health_msg' : health_msg,
                            'latest_tweet' : latest_tweet,
                            'twitter_error': 0 } 
    except TwythonError:
        json_return_val = { 'twitter_error': 1 }
            
    return HttpResponse(json.dumps(json_return_val), mimetype="application/json")
    
# Private Methods
def _twitter_display_context(request):
    """
    This is a function that displays the homepage for someone who has already
    signed in with Twitter.  The twitter details of the user will be stored in
    the session.
    """
    context = { }
    
    try:
        context.update({'twitter_username' : request.session['twitter_info']['screen_name']})
    
    except KeyError:
        return HttpResponseRedirect(settings.AUTHORIZE_COMPLETE_URL)
                    
    return context

def _get_twitter_data(request):
    """
    This function is the one that interacts with Twitter's REST API to
    get the user's timeline of tweets to assess the health rating.
    """    
    try:
        twitter = Twython(
            twitter_token = settings.TWITTER_KEY,
            twitter_secret = settings.TWITTER_SECRET,
            oauth_token = request.session['twitter_info']['oauth_token'],
            oauth_token_secret = request.session['twitter_info']['oauth_token_secret'],
        )
    
    # KeyError(s) here indicate the user clicking cancel instead of signing in
    except KeyError:
        return HttpResponseRedirect(settings.AUTHORIZE_COMPLETE_URL)
    
    user_timeline = twitter.getUserTimeline()
    
    if user_timeline:
        latest_tweet = user_timeline[0]
    else:
        latest_tweet = ''
    
    # Determine the health rating
    new_health_rating = _determine_health_rating(
        user_timeline=user_timeline,
        home_timeline=twitter.getHomeTimeline()
    )
    
    # from IPython import embed; embed()

    return new_health_rating, latest_tweet
    
def _determine_health_rating(user_timeline=None, home_timeline=None):
    """
    This function specifically deals with assessing a person's health
    rating based on their twitter data and returning this value.
    """
    if user_timeline is None and home_timeline is None:
        return 5
    else:
        return 0
        