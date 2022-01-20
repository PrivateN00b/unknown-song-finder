from locale import currency
import re
from tokenize import Double
from typing import List
from urllib import response
import requests
import json
import re

class SongFinder:
    
    def __init__(self, token, minPopularity, maxPopularity, amount):
            self.token = token
            self.minPopularity = minPopularity
            self.maxPopularity = maxPopularity
            self.amount = amount
      
    @property     #Getter     
    def songList(self):
        newReleases = self.GetNewReleases(None, self.amount)
        songList = list()
            
        for i in newReleases["albums"]["items"]:   
            songList.append(self.SongListAppend(i["href"], self.minPopularity, self.maxPopularity))
        
        return songList
                
    def ReturnSongList(self, songList):
        return songList
                    
    def GetAPI(self, GET):
        response = requests.get(GET,
        headers={
            "Authorization": f"Bearer {self.token}"
            }
        )
        jsonResponse = response.json()
    
        return jsonResponse   
            
    def GetNewReleases(self, market, amount):
        newReleasesURL = ""
        
        if market is None: 
            newReleasesURL = f"https://api.spotify.com/v1/browse/new-releases?limit={amount}"
        else:
            newReleasesURL = f"https://api.spotify.com/v1/browse/new-releases?country={market}&limit={amount}"
            
        return self.GetAPI(newReleasesURL)
    
    def GetTrackPopularity(self, trackID):
        trackJson = self.GetAPI(f"	https://api.spotify.com/v1/tracks/{trackID}")
        return trackJson["popularity"]
      
    def SongListAppend(self, albumURL, minPopularity, maxPopularity):
        albumJson = self.GetAPI(albumURL)
        
        if albumJson["popularity"] > minPopularity and albumJson["popularity"] < maxPopularity:
            albumTracksURL = f"{albumURL}/tracks"
            albumTracksJson = self.GetAPI(albumTracksURL)
            mostPopularSong = None
            
            for i in albumTracksJson["items"]:
                currentPopularity = self.GetTrackPopularity(i["id"])
                mostPopularity = 0
                
                if currentPopularity > mostPopularity:
                    mostPopularity = currentPopularity
                    mostPopularSong = i["id"]
                    
            return mostPopularSong
                
          
        
            
    