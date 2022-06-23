import csv
from dataclasses import dataclass
from datetime import date
from genericpath import exists
from time import sleep
from types import NoneType
from typing import List
from unittest import result
from urllib import response
from urllib.parse import urlencode
from matplotlib.text import OffsetFrom
from nbformat import write
import requests
import json
import base64

from Auth import Auth

@dataclass
class SpotifySongGatherer:
    
    # Some global variables/attributes
    auth: Auth = None # This class contains an authorize method
    
    def __init__(self, auth: Auth):
        self.auth = auth
        self.auth.Authorize()
       
    def SearchTracks(self, q: str, tp: list, market: str, offset: int, limit: int):
        """Search for tracks duuuh 

        Args:
            q (str): Query filters
            tp (list): Types
            market (str): Country code
            offset (int): If you don't want the first results you can deviate with this
            limit (int): Amount of results you want (0<=x<=50)

        Returns response's JSON object
        """
        # Creating query URL
        queryUrl = f"?q={q}&offset={offset}&limit={limit}"
        for currentType in tp:
            queryUrl += f"&type={currentType}"
        if market is not NoneType:
            queryUrl += f"&market={market}"
        
        # Initiaiting GET request
        response = requests.get(
                    url=f"https://api.spotify.com/v1/search{queryUrl}",
                    headers={
                    "Authorization": f"{self.auth.tokenType} {self.auth.accessToken}"
                    })    
        return response.json()
    
    def GetTracksAudioFeatures(self, ids):
        queryUrl = f"?ids={ids}"
        response = requests.get(
            url=f"https://api.spotify.com/v1/audio-features{queryUrl}",
            headers={
            "Authorization": f"{self.auth.tokenType} {self.auth.accessToken}"
            })
        return response.json()
        
    # Gets all of the avalaible genres
    def GetAvalaibleGenreSeeds(self):
        response = requests.get(
            url='https://api.spotify.com/v1/recommendations/available-genre-seeds',
            headers={
            'Authorization': f"{self.auth.tokenType} {self.auth.accessToken}"
            }
        )
        return response.json()
        


    # Adds precious datas to a csv file
    def AddToCSV(self, tracksToAdd, tracksAudioFeatures):
        # Checks if the tracks.csv file exists
        if not exists('tracks.csv'):
            with open('tracks.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'name', 'danceability', 'energy', 'key',
                                'loudness', 'mode', 'speechiness', 'acousticness',
                                'instrumentalness', 'liveness', 'valence', 'tempo',
                                'time_signature'])   
        else:
            with open('tracks.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                uniqueTracks = list()
                
                # Checks for tracks which have already been added to avoid duplicates
                if tracksAudioFeatures['audio_features'] is not None:
                    for i in range(len(tracksAudioFeatures['audio_features'])):
                        with open('tracks.csv', 'r', encoding='utf-8') as file:
                            trackItemRow = tracksToAdd['tracks']['items'][i]
                            trackFeatureRow = tracksAudioFeatures['audio_features'][i]
                            if trackFeatureRow['id'] not in file.readlines():
                                uniqueTracks.append(f"{trackItemRow['id']},{trackItemRow['name']},{trackFeatureRow['danceability']},{trackFeatureRow['energy']},{trackFeatureRow['key']},{trackFeatureRow['loudness']},{trackFeatureRow['mode']},{trackFeatureRow['speechiness']},{trackFeatureRow['acousticness']},{trackFeatureRow['instrumentalness']},{trackFeatureRow['liveness']},{trackFeatureRow['valence']},{trackFeatureRow['tempo']},{trackFeatureRow['time_signature']}")    

                # Adding the non-duplicates to the file
                for currentTrack in uniqueTracks:
                    writer.writerow([currentTrack])
                uniqueTracks.clear()               
                
    # Starts calling SearchTracks for all years between 1980-(insert current year here) and specific genres to find a bunch of songs
    # genresToAvoid: Genres that are excluded from SearchTracks API
    def BeginTrackSearchAndUploading(self, genresToAvoid):
        # Removing genres that aren't acceptable
        goodGenres = set(self.GetAvalaibleGenreSeeds()['genres']) - set(genresToAvoid)
        # Iterating through a bunch of years and genres and offsetting
        for currentYear in range(1980, date.today().year):
            for currentGenre in goodGenres:
                offset = 0
                while offset < 5000: 
                    # Tracks and some data about them
                    tracksToAdd = self.SearchTracks(q=f"year:{currentYear}%20genre:{currentGenre}", tp=['track'], market='US', offset=offset, limit=50)
                    offset += int(tracksToAdd['tracks']['limit'])
                    # Tracks's audio features which are probably used by recommendation algorithms
                    trackIDs = str()
                    for currentTrack in tracksToAdd['tracks']['items']:
                        trackIDs += f"{currentTrack['id']}%2C"
                    trackIDs = trackIDs[:-3]
                    tracksAudioFeatures = self.GetTracksAudioFeatures(trackIDs)
                    # tracksAudioFeatures = GetTracksAudioFeatures(tracksToAdd['tracks']['items'])
                    self.AddToCSV(tracksToAdd, tracksAudioFeatures)
                    sleep(1)
    
    