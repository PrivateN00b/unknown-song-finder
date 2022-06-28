from abc import ABC, abstractmethod
import base64
from dataclasses import dataclass
import json
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
from scipy.fftpack import sc_diff
import keyring

@dataclass
class Auth(ABC):
    """A base class for creating authorization clases."""
    
    # Some global variables/attributes
    clientID: str = 'cbef85907193457e978b1fe28885af1d' # Necessary for auth
    clientSecret: str = '88d40f75396c4a1cafc7b9e56040593d' # Necessary for auth
    tokenURL: str = "https://accounts.spotify.com/api/token" # Authorization API URL
    token: dict = None # The token from the authorization with it's refresh, expiration etc. variables
    
    @abstractmethod
    def Authorize(self):
        """Makes the authorization.
        
        Types: Client Credentials, Code Flow
        """
        pass
    
    @abstractmethod
    def RefreshToken(self):
        """Refreshes token duuh."""
        pass

@dataclass
class AuthClientCredentials(Auth):
    """Spotify authorization with Client Credentials.
        https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/"""
    def __init_subclass__(cls):
        return super().__init_subclass__()
    
    def Authorize(cls):
        responseAuth = requests.post(
            url=cls.tokenURL, # Where we wanna authorize
            headers={
                'Authorization': f"Basic {base64.b64encode((cls.clientID+':'+cls.clientSecret).encode()).decode()}"
            }, # Header parameters
            data={
                'grant_type': 'client_credentials'
            }, # Body parameters
            json=True
            )
        # Grants data to accessToken, tokenType, expiresIn
        cls.token = responseAuth.json()
    
    def RefreshToken(cls):
        responseAuth = requests.post(
            url=cls.tokenURL, # Where we wanna authorize
            headers={
                'Authorization': f"Basic {base64.b64encode((cls.clientID+':'+cls.clientSecret).encode()).decode()}"
            }, # Header parameters
            data={
                'grant_type': 'refresh_token',
                'refresh_token': cls.token['refresh_token']
            }, # Body parameters
            json=True
            )
        cls.token = responseAuth.json()

@dataclass
class AuthCode(Auth):
    """Spotify authorization with Code Flow.
       https://developer.spotify.com/documentation/general/guides/authorization/code-flow/"""
    
    redirectURI: str = "https://noobkozlegeny.github.io"
    authorizationBaseURL: str = "https://accounts.spotify.com/authorize"
    # Scopes gives rights to do special API calls like getting current user's info
    # https://developer.spotify.com/documentation/general/guides/authorization/scopes/
    scope = [
        "user-read-email",
        "playlist-read-collaborative",
        "playlist-modify-public",
        "playlist-modify-private"
    ]
    
    def __init_subclass__(cls):
        return super().__init_subclass__()
    
    def Authorize(cls):
        
        tokenFromKeyring = keyring.get_credential(service_name="spotify-authcode", username="Oyasumi")
        
        # Checking if the authorization have already been made by checking the keyring file
        if keyring.get_credential(service_name="spotify-authcode", username="Oyasumi") is None:
            spotify = OAuth2Session(cls.clientID, scope=cls.scope, redirect_uri=cls.redirectURI)

            # Redirect user to Spotify for authorization
            authorizationURL, state = spotify.authorization_url(cls.authorizationBaseURL)
            print('Please go here and authorize: ', authorizationURL)

            # Get the authorization verifier code from the callback url
            redirect_response = input('\n\nPaste the full redirect URL here: ')

            auth = HTTPBasicAuth(cls.clientID, cls.clientSecret)

            # Get the token data from the URL and assign the results to tokenType, accessToken and expiresIn
            token = spotify.fetch_token(cls.tokenURL, auth=auth, authorization_response=redirect_response)
            cls.token = token
            
            # Putting the token into the host OS's keyring file which is encrypted
            keyring.set_password(service_name="spotify-authcode", username="Oyasumi", password=json.dumps(token))
        else:
            cls.token = json.loads(tokenFromKeyring.password)
            # keyring.delete_password(service_name="spotify-authcode", username="Oyasumi")
            
    def RefreshToken(cls):
        responseAuth = requests.post(
            url=cls.tokenURL,
            headers={
                'Authorization': f"Basic {base64.b64encode((cls.clientID+':'+cls.clientSecret).encode()).decode()}"
            }, # Header parameters
            data={
                'grant_type': 'refresh_token',
                'refresh_token': cls.token['refresh_token']
            }, # Body parameters
            json=True
            )
        cls.token = responseAuth.json()
