from locale import currency
import re
from typing import List
from unittest import result
from urllib import response
# from attr import dataclass
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
        """Returns the current user's ID response"""
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
        """Returns the current user's playlists response"""
        response = requests.get(self.PlaylistsURL,
            headers={
                'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
                })

        return response

    def CreatePlaylist(self, name: str, desc: str):
        """Creates a playlist for the current user"""
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
        
        return response

    # Doesn't return bool to also get the playlistID
    def DoesPlayListExists(self, name: str):
        """Checks if the current user already has an X named playlist.

        Args:
            name (str): The playlist name we want to check if it exists

        Returns:
            if playlist exists: The playlist's ID
            if playlist doesn't: None
        """
        responseJson = self.GetExistingPlaylists().json()
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
    
    def AddToPlaylist(self, playlistID: str, tracks: list):
        """Add tracks to playlist
        
        Args:
            playlistID (str): The playlist's ID
            tracks (list): List containing ID's of tracks

        Returns: Response""" 
             
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
        
        return response       
    
    def ChangePlaylistDetails(self, name: str, desc: str, playlistID: str = None):
        """Changes a playlist's details. If a playlistID haven't been added then it fill try to find
        the playlist's ID which has the same name as in the parameter name.

        Args:
            name (str): Playlist's name
            desc (str): Playlist's description
            playlistID (str, optional): Playlist's ID. If None then it fill try to find
                the playlist's ID which has the same name as in the parameter name.

        Returns: 
            If playlist exists: Response
            If playlist doesn't exists: False
        """
        
        if playlistID is None:
            playlistID = self.DoesPlayListExists(name)
        
        if playlistID is not None:
            response = requests.put(f"https://api.spotify.com/v1/playlists/{playlistID}",
                headers={
                    'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
                    },
                json={
                    "name": name,
                    "public": True,
                    "description": desc
                }
            )
        else:
            return False
        
        return response