from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from twython import Twython

"""
    Public Methods
"""
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

"""
    Private Methods
"""

def _twitter_display_context(request):
    """

    """
    twitter = Twython(
        twitter_token = settings.TWITTER_KEY,
        twitter_secret = settings.TWITTER_SECRET,
        oauth_token = request.session['twitter_info']['oauth_token'],
        oauth_token_secret = request.session['twitter_info']['oauth_token_secret'],
    )

    context = { 'twitter_username' : request.session['twitter_info']['screen_name'] }
    return context
