import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings

from twython import Twython, TwythonError
import twitter as twit

# Constants
HEALTHY_WORDS = ['gym','salad','walking','marathon','running','fitness']
UNHEALTHY_WORDS = ['pizza','restaurant','dessert','beer','alcohol']

# Public Methods
def homepage(request):
    """
    This function is reponsible for displaying the homepage for
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
    This function is reponsible for displaying the about page for
    TweetHealth.
    """
    return render_to_response(
            'about.html',
            context_instance=RequestContext(request))

def update_health_rating(request):
    """
    This function is a callback from a POST request
    sent from the user's browser.  This will be triggered periodically.
    """
    context = { }
    
    try:
        health_rating, latest_tweet = _get_twitter_data(request)
        
        # save new health rating into the user's session for later use
        request.session['health_rating'] = health_rating
        
        # determine string to display based on health
        if health_rating == 0:
            health_msg = 'Do you like not use Twitter? Not cool.'
        elif health_rating > 0 and health_rating <= 50:
            health_msg = 'Meh...you could do better..hit the gym buddy.'
        elif health_rating > 50 and health_rating <= 80:
            health_msg = 'You\'re okay, but not super healthy.'
        else:
            health_msg = 'Good for you...you work out and eat well.'
        
        context.update({'health_rating' : health_rating,
                        'health_msg' : health_msg,
                        'latest_tweet' : latest_tweet})
        
        html_string = render_to_string(
                                  'twitter_health_info.html',
                                  context,
                                  context_instance=RequestContext(request))

        json_return_val = { 'html_string' : html_string,
                            'twitter_error': 0 }     
                                
    # catch various Twitter API errors, (401 is auth error, 403 is rate limit error)
    except TwythonError as e:
        if e.error_code == 401:
            json_return_val = { 'twitter_error': 1,
                                'auth_error': 1 }
        elif e.error_code == 403:
            json_return_val = { 'twitter_error': 1,
                                'rate_error': 1 }
        else:
            json_return_val = { 'twitter_error': 1 }
        
    return HttpResponse(json.dumps(json_return_val), mimetype="application/json")

def post_tweet(request):
    """
    This function posts a tweet of your TweetHealth to Twitter.  This function
    uses a different Twitter library called twitter since Twython only seems
    to be working with GET requests.
    """
    try:
        t = twit.Twitter(
            auth=twit.OAuth(request.session['twitter_info']['oauth_token'],
            request.session['twitter_info']['oauth_token_secret'],
            settings.TWITTER_KEY,settings.TWITTER_SECRET)
        )
        tweet_msg = 'My TweetHealth score is ' + str(request.session['health_rating'])
        t.statuses.update(status=tweet_msg)
        
    # KeyError here indicates health rating was not saved properly into the session
    except KeyError:
        return HttpResponseRedirect(settings.AUTHORIZE_COMPLETE_URL)
    # TwitterHTTPError indicates an error interacting with Twitter's API
    except twit.TwitterHTTPError as e:
        json_return_val = { 'tweet_error': 1,
                            'latest_tweet': 'Error posting tweet' }
        
    json_return_val = { 'latest_tweet' : tweet_msg,
                        'tweet_error' : 0 }

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
    
    # KeyError(s) here indicate the user clicking cancel instead of signing in
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
        latest_tweet = user_timeline[0]['text']
    else:
        latest_tweet = ''

    # Determine the health rating
    new_health_rating = _determine_health_rating(
        user_timeline=user_timeline
    )
    
    return new_health_rating, latest_tweet
    
def _determine_health_rating(user_timeline=None):
    """
    This function specifically deals with assessing a person's health
    rating based on their twitter data and returning this value.
    """    
    # start at a 75 (an average ealth score)
    health_meter = 75
    
    if not user_timeline:
        # set to zero, this person does not really use twitter cannot give average score of 75
        health_meter = 0
    else:
        # list comprehensions to determine healthy and unhealthy points
        healthy_points = len([(tweet,word) for tweet in user_timeline for word in HEALTHY_WORDS if word in tweet['text']])
        unhealthy_points = len([(tweet,word) for tweet in user_timeline for word in UNHEALTHY_WORDS if word in tweet['text']])
    
        # Alter score based on points calculated
        health_meter += healthy_points*10
        health_meter -= unhealthy_points*10
        
    # if somehow score gets below 0 or above 100, set it to 10 or 100
    if health_meter < 0:
        health_meter = 10
    elif health_meter > 100:
        health_meter = 100
        
    return health_meter
