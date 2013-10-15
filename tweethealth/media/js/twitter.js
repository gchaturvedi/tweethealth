/**
  * This file holds the functions which interact with TweetHealth's server
  * which triggers view functions related to Twitter
  */

/* this function is called periodically to update the user's TweetHealth score */
function twitterUpdate() {
    $.ajax({
        type: "POST",
        url: '/twitter/update-timeline/',
        success:  function(data) {
			if(data['twitter_error']) {
				$('.tweet-score-container').hide();
				$('.latest-tweet').hide();
				$('.waiting-block').hide();
				$('.tweet-button-container').hide();

				if(data['rate_error']) {
					$('.twitter-block').text('You have hit the Twitter API rate limit.');
				}
				else if (data['auth_error']) {
					$('.twitter-block').html('You do not have the proper authentication with Twitter or have revoked access to the TweetHealth app.  Please <a href="/login/">relogin here</a>.');
				}
				else {
					$('.twitter-block').text('Unable to fetch Twitter data.  Please try again later.');
				}
			}
			else {
				$('.twitter-block').html(data['html_string']);
				$('.waiting-block').hide();
			}
        },
        error: function(data) {
			// Insert error processing here if necessary
        }
	});
}

/* This function is called to tweet the TweetHealth rating and its triggered by the user */
function postTweet() {
    $.ajax({
        type: "POST",
        url: '/twitter/post-tweet/',
        success:  function(data) {
			$('.latest-tweet').text(data['latest_tweet']);

			if(data['twitter_error']) {
				$('.latest-tweet-label').hide();
        $('.post-error').show();
        $('.btn-large').hide();
        if(data['duplicate_error']) {
          $('.post-error').text('You just tweeted this already!')
        } else {
          $('.post-error').text('Somethin or another went wrong!')
        }
			}
			else {
				$('.latest-tweet-label').text('Tweet posted!');
				$('.latest-tweet').text(data['latest_tweet']);
				$('.btn-large').hide();
			}
        },
        error: function(data) {
			// Insert error processing here if necessary
        }
	});
}
