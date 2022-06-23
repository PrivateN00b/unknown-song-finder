from tkinter.messagebox import NO
import requests
from Auth import Auth

class SpotifyRecommendation:
    
    auth: Auth = None
    
    def __init__(self, auth: Auth, seedArtists, seedGenres, seedTracks):
        self.auth = auth
        self.auth.Authorize()
    
    # Spotify's recommendation API
    def GetRecommendations(self):
        response = requests.get(
        url='https://api.spotify.com/v1/recommendations',
        headers={
            'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
        },
        json={
            #Need to get seed data
        })