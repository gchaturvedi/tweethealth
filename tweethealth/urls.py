from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.static import serve

from tweethealth import views
from tweethealth.utils import twitter_oauth

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # serve static media content
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # View that handles what to display on homepage
    (r'^$', views.homepage),

    # Twitter related URLs
    url(r'^login/?$', twitter_oauth.connect),
    url(r'^login-confirm/?$', twitter_oauth.authorized),
)
