from locale import currency
import re
from typing import List
from unittest import result
from urllib import response
import requests
import json

from SongFinder import SongFinder

#Spotify base API: https://api.spotify.com/v1/

#Insert your userID in the userID variable
#How to get userID: Spotify -> Account -> copy the username with the random strings
userID = "Hey Gleb, did you take a paper clip?"
PlaylistsURL = f"https://api.spotify.com/v1/users/{userID}/playlists"
#Go to and get token: https://developer.spotify.com/console/post-playlist-tracks/?playlist_id=&position=&uris=
token = "BQCLRwlLSkof53Rwl14DUPFalUtJ0bBwUcwf31A9f7y1Ks49GotZT3-GY0M7D12YGpzHZnVBJhTonsBS0ZDf0XcCK_U6rayvMqElR3G11CWNyXu22J7w-w-x_gb7_0QoM1zIVOE2jXSBsZ-J_ZjfqWSGvkcnxXdDKAQsRvi0dzxuVzt2r9vtGPL5uf4rA6kKcKniQuQDyeW9BfHdyzxiGQQBrMww9VmxdlxeoaLh8Pq5zA"

def GetExistingPlaylists():
    response = requests.get(PlaylistsURL,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    jsonResponse = response.json()
    
    return jsonResponse

def CreatePlaylist(name):
    response = requests.post(PlaylistsURL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": name,
            "public": True,
            "description": "Finding unknown songs duuh"
        }
    )
    jsonResponse = response.json()
    
    return jsonResponse

#Doesn't return bool to also get the playlistID
def DoesPlayListExists(name):
    responseJson = GetExistingPlaylists()
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
 
#TODO: For some reason when the playlist doesn't yet exist and only will be created on-the-run the songs won't be there first.
# (Just an empty playlist, but the songs will be added on an existing one)
def AddToPlaylist(playlistID):
    #Finding the songs
    sf = SongFinder(token, 0, 80, 30) #Really slow to finish
    songlist = sf.songList
    
    #Adding the songs  
    postURL = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?uris="
    postURL += f"spotify%3Atrack%3A{songlist[0]}"
    
    for i in range(1, len(songlist)):
        postURL += f"%2Cspotify%3Atrack%3A{songlist[i]}"
    
    response = requests.put(postURL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "range_start": 1,
            "insert_before": 3,
            "range_length": 2
        }
    )
    jsonResponse = response.json()
    
    return jsonResponse  

def main():
    name = "Unknown Songs"
    playlistID = DoesPlayListExists(name) #Returns playlistID or None
    
    #Creating Playlist and checking if it already exists
    if playlistID is None:
        playlist = CreatePlaylist(name)
    else:
        print("Playlist already exists!")
    
    #Adding songs
    AddToPlaylist(playlistID)
    
    print("Successful!")
    
if __name__ == "__main__":
    main()