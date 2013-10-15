from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.handlers.base import BaseHandler
from django.test.client import RequestFactory

from twython import Twython

def connect(request):
    """
    This function begins the three legged oAuth handshake between
    TweetHealth and Twitter.
    """
    if settings.LOCAL_ENVIRONMENT:
        twitter_callback = 'http://localhost:8000/login-confirm/'
    else:
        twitter_callback = 'http://tweethealth.heroku.com/login-confirm/'

    twitter = Twython(
        settings.TWITTER_KEY,
        settings.TWITTER_SECRET,
    )

    auth = twitter.get_authentication_tokens(callback_url=twitter_callback)

    # get the initial round of the three legged oauth tokens
    auth_dict = twitter.get_authentication_tokens(callback_url=twitter_callback)

    request.session['request_token'] = auth_dict
    return HttpResponseRedirect(auth_dict['auth_url'])

def authorized(request, redirect_url=settings.AUTHORIZE_COMPLETE_URL):
    """
    This function is a callback from Twitter which is triggered after
    the user signs in and allows authorization of their Twitter account.
    """
    try:
        twitter = Twython(
            settings.TWITTER_KEY,
            settings.TWITTER_SECRET,
            request.session['request_token']['oauth_token'],
            request.session['request_token']['oauth_token_secret'],
        )
        # Get the access token to complete the three legged oauth handshake
        twitter_info = twitter.get_authorized_tokens(request.GET['oauth_verifier'])

    # Something unusual happened from the redirect back from twitter and
    # nothing was stored in the session, redirect back to homepage.
    except KeyError:
        return HttpResponseRedirect(redirect_url)

    # only store twitter info in the session if its valid otherwise the user
    # hit cancel and didn't actually sign in
    if 'oauth_token_secret' in twitter_info and 'user_id' in twitter_info:
        request.session['twitter_info'] = twitter_info

    return HttpResponseRedirect(redirect_url)
