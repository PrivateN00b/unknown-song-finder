from locale import currency
import re
from typing import List
from unittest import result
from urllib import response
from attr import dataclass
import requests
import json

from SpotifyScripts.Auth import Auth

class PlayListUpdater:
    
    auth: Auth = None

    #Spotify base API: https://api.spotify.com/v1/    
    #Insert your userID in the userID variable
    #How to get userID: Spotify -> Account -> copy the username with the random strings
    userID: str = "Hey Gleb, did you take a paper clip?" # This will get overriden in the __init__.
    PlaylistsURL: str = "*Insert Graphic design is my passion meme*"
    
    def GetCurrentUserID(self):
        response = requests.get(
            url='https://api.spotify.com/v1/me',
            headers={
                'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
                })
        
        return response.json()['id']
    
    def __init__(self, auth: Auth):
        self.auth = auth
        self.auth.Authorize()
        self.auth.RefreshToken()
        self.userID = self.GetCurrentUserID()
        self.PlaylistsURL = f"https://api.spotify.com/v1/users/{self.userID}/playlists"
    
    def GetExistingPlaylists(self):
        response = requests.get(self.PlaylistsURL,
            headers={
                'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
                })
        
        return response.json()

    def CreatePlaylist(self, name: str, desc: str):
        response = requests.post(self.PlaylistsURL,
            headers={
                'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
                },
            json={
                "name": name,
                "public": True,
                "description": desc
            }
        )
        jsonResponse = response.json()
        
        return jsonResponse

    # Doesn't return bool to also get the playlistID
    def DoesPlayListExists(self, name: str, description: str):
        responseJson = self.GetExistingPlaylists()
        exists = False
        result = None
        i = 0
        
        while exists == False and i < len(responseJson["items"]):
            current = responseJson["items"][i]
            
            if current["name"] == name:
                exists = True
                result = current["id"]
            i += 1
            
        return result           
    
    # TODO: For some reason when the playlist doesn't yet exist and only will be created on-the-run the songs won't be there first.
    # (Just an empty playlist, but the songs will be added on an existing one)
    def AddToPlaylist(self, playlistID, tracks: list):       
        #Adding the songs  
        postURL = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?uris="
        postURL += f"spotify%3Atrack%3A{tracks[0]}"
        
        for i in range(1, len(tracks)):
            postURL += f"%2Cspotify%3Atrack%3A{tracks[i]}"
        
        response = requests.put(postURL,
            headers={
                'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
                },
            json={
                "range_start": 1,
                "insert_before": 3,
                "range_length": 2
            }
        )
        
        return response.json()  