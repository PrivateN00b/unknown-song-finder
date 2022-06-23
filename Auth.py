from abc import ABC, abstractmethod
import base64
from dataclasses import dataclass
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
from scipy.fftpack import sc_diff

@dataclass
class Auth(ABC):
    
    # Some global variables/attributes
    clientID: str = 'cbef85907193457e978b1fe28885af1d' # Necessary for auth
    clientSecret: str = '88d40f75396c4a1cafc7b9e56040593d' # Necessary for auth
    tokenURL: str = "https://accounts.spotify.com/api/token" # Authorization API URL
    token: dict = None # The token from the authorization with it's refresh, expiration etc. variables
    
    @abstractmethod
    def Authorize(self):
        pass

@dataclass
class AuthClientCredentials(Auth):
    
    def Authorize(self):
        responseAuth = requests.post(
            url=self.tokenURL, # Where we wanna authorize
            headers={
                'Authorization': f"Basic {base64.b64encode((self.clientID+':'+self.clientSecret).encode()).decode()}"
            }, # Header parameters
            data={
                'grant_type': 'client_credentials'
            }, # Body parameters
            json=True
            )
        # Grants data to accessToken, tokenType, expiresIn
        responseResult = responseAuth.json()
        token = responseResult

@dataclass
class AuthCode(Auth):
    """Spotify authorization with Code Flow.
       https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
    """
    
    redirectURI: str = "https://noobkozlegeny.github.io"
    authorizationBaseURL: str = "https://accounts.spotify.com/authorize"
    # Scopes gives rights to do special API calls like getting current user's info
    # https://developer.spotify.com/documentation/general/guides/authorization/scopes/
    scope = [
        "user-read-email",
        "playlist-read-collaborative"
    ]
    
    def Authorize(self):       
        spotify = OAuth2Session(self.clientID, scope=self.scope, redirect_uri=self.redirectURI)

        # Redirect user to Spotify for authorization
        authorizationURL, state = spotify.authorization_url(self.authorizationBaseURL)
        print('Please go here and authorize: ', authorizationURL)

        # Get the authorization verifier code from the callback url
        redirect_response = input('\n\nPaste the full redirect URL here: ')

        auth = HTTPBasicAuth(self.clientID, self.clientSecret)

        # Get the token data from the URL and assign the results to tokenType, accessToken and expiresIn
        token = spotify.fetch_token(self.tokenURL, auth=auth, authorization_response=redirect_response)
        self.token = token
