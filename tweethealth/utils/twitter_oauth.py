from django.http import HttpResponseRedirect
from django.conf import settings

from twython import Twython

def connect(request):
    """
    This method begins the three legged oAuth handshake between
    TweetHealth and Twitter.
    """
    if settings.LOCAL_ENVIRONMENT:
        twitter_callback = 'http://localhost:8000/login-confirm/'
    else:
        twitter_callback = 'http://tweethealth.heroku.com/login-confirm/'
        
    twitter = Twython(
        twitter_token = settings.TWITTER_KEY,
        twitter_secret = settings.TWITTER_SECRET,
        callback_url = twitter_callback
    )

    auth_dict = twitter.get_authentication_tokens()

    request.session['request_token'] = auth_dict
    return HttpResponseRedirect(auth_dict['auth_url'])

def authorized(request, redirect_url=settings.AUTHORIZE_COMPLETE_URL):
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
    
    # Get the access token to complete the three legged oAuth handshake
    twitter_info = twitter.get_authorized_tokens()
    
    if 'oauth_token_secret' in twitter_info and 'user_id' in twitter_info:
        request.session['twitter_info'] = twitter_info
    
    return HttpResponseRedirect(redirect_url)
