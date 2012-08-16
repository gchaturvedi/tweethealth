from django.conf.urls import patterns, include, url
from tweethealth import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

	# View that handles what to display on homepage
    (r'^$', views.homepage),
	
	# Twitter related URLs
	url(r'^login/?$', views.twitter_connect),
	url(r'^login-confirm/?$', views.twitter_authorized),
)
