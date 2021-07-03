from tweepy import API, OAuthHandler
import credentials


class Authentication:
    """
    This class sets user credentials (credencials.py) and access tokens.
    """
    def authenticate(self):
        auth = OAuthHandler(credentials.consumer_Key, credentials.consumer_secret);
        auth.set_access_token(credentials.access_token, credentials.token_secret);
        return auth;
