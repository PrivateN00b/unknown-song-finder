import csv
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

# Some global variables
clientID = 'a32a39b5f60b45ef8fe83a2d63f7bd8e' # Necessary for auth
clientSecret = '74dbf39966bf4daab76662d946107a06' # Necessary for auth
accessToken = "" # Token from the auth response
tokenType = "" # Token type from the auth response
expiresIn = 0 # This token will expire in x seconds
    
# Authorization with Client Credentials Flow
def AuthorizeWithClientCredentials():
    responseAuth = requests.post(
        url='https://accounts.spotify.com/api/token', # Where we wanna post
        headers={
            'Authorization': f"Basic {base64.b64encode((clientID+':'+clientSecret).encode()).decode()}"
        }, # Header parameters
        data={
            'grant_type': 'client_credentials'
        }, # Body parameters
        json=True
        )
    # Grants data to accessToken, tokenType, expiresIn
    responseResult = responseAuth.json()
    global accessToken, tokenType, expiresIn
    accessToken = responseResult['access_token']   
    tokenType = responseResult['token_type']
    expiresIn = responseResult['expires_in']  
    
# Search for tracks duuuh
def SearchTracks(q, tp, market, offset, limit):
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
                "Authorization": f"{tokenType} {accessToken}"
                }
                # params={
                #     "q": q,
                #     "type": tp,
                #     "market": market,
                #     "limit": limit
                # }
                )    
    return response.json()
 
def GetTracksAudioFeatures(ids):
    queryUrl = f"?ids={ids}"
    response = requests.get(
        url=f"https://api.spotify.com/v1/audio-features{queryUrl}",
        headers={
           "Authorization": f"{tokenType} {accessToken}"
        })
    return response.json()
     
# Gets all of the avalaible genres
def GetAvalaibleGenreSeeds():
    response = requests.get(
        url='https://api.spotify.com/v1/recommendations/available-genre-seeds',
        headers={
           'Authorization': f"{tokenType} {accessToken}"
        }
    )
    return response.json()
    
# Spotify's recommendation API
def GetRecommendations():
    response = requests.get(
       url='https://api.spotify.com/v1/recommendations',
       headers={
           'Authorization': f"{tokenType} {accessToken}"
       },
       json={
           #Need to get seed data
       }
    )

# Adds precious datas to a csv file
def AddToCSV(tracksToAdd, tracksAudioFeatures):
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
def BeginTrackSearchAndUploading(genresToAvoid):
    # Removing genres that aren't acceptable
    goodGenres = set(GetAvalaibleGenreSeeds()['genres']) - set(genresToAvoid)
    # Iterating through a bunch of years and genres and offsetting
    for currentYear in range(1980, date.today().year):
        for currentGenre in goodGenres:
            offset = 0
            while offset < 5000: 
                # Tracks and some data about them
                tracksToAdd = SearchTracks(q=f"year:{currentYear}%20genre:{currentGenre}", tp=['track'], market='US', offset=offset, limit=50)
                offset += int(tracksToAdd['tracks']['limit'])
                # Tracks's audio features which are probably used by recommendation algorithms
                trackIDs = str()
                for currentTrack in tracksToAdd['tracks']['items']:
                    trackIDs += f"{currentTrack['id']}%2C"
                trackIDs = trackIDs[:-3]
                tracksAudioFeatures = GetTracksAudioFeatures(trackIDs)
                # tracksAudioFeatures = GetTracksAudioFeatures(tracksToAdd['tracks']['items'])
                AddToCSV(tracksToAdd, tracksAudioFeatures)
                sleep(1)
        
        
def main():
    AuthorizeWithClientCredentials()
    BeginTrackSearchAndUploading(genresToAvoid=[
        'ambient', 'bluegrass', 'bossanova', 'children', 'country', 'gospel',
        'indian', 'iranian', 'kids', 'malay', 'mandopop', 'mpb', 'opera', 'pagode',
        'philippines-opm', 'rainy-day', 'sertanejo', 'sleep', 'study', 'turkish'
        ])
    
    
if __name__ == '__main__':
    main()
    
    