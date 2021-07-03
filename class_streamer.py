from tweepy import API, Cursor, Stream
from class_auth import Authentication


class Streamer:
    """
    This class creates an instance (self.auth) that inherits from Class Authentication / Method authenticate(), which validates user credentials.
    Then search for tweets related to the given keywords.
    """
    def __init__(self):
        self.auth = Authentication();
        self.api = API(self.auth.authenticate(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True);

    def find_keyword(self, keyword_to_find):
        """
        This function searches for tweets that contain any of the given words.
        Rate limits: 450 requests / 15 min (app auth / API Standard v1.1).
        """
        tweets_list = [];
        for tweet in Cursor(self.api.search, q=keyword_to_find, lang="es", result_type="recent", tweet_mode="extended").items(100):
            tweets_list.append(tweet);

        return tweets_list;
