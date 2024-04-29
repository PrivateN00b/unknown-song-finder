import requests
from SpotifyScripts.Auth import Auth
from SpotifyScripts.CustomExceptions import *
from pubsub import pub

class SpotifyRecommendation:
    
    auth: Auth = None
    
    # Dirty code but this is needed to somehow store when the user selects the correct track and the ID will be sent by the SelectCorrectTrackID in Main.py
    selectedTrackID: str = None
    
    def __init__(self, auth: Auth):
        self.auth = auth
        self.auth.Authorize()
        # self.auth.RefreshToken()
        pub.subscribe(self.RerunCorrectTrackSearch ,'rerunCorrectTrackSearch')
    
    def GetSelectedTrackID(self, selectedID: str):
        self.selectedTrackID = selectedID
    
    def RerunCorrectTrackSearch(self, item: str, type: str, offset: int):
        self.DoesItemExists(item, type, offset)
    
    def GetItemIDs(self, data: dict):
        """Selects the IDs from the dictionary JSON object and returns it."""
        
        recommendedTrackIDs = list()
        for currentTrack in data['tracks']:
            recommendedTrackIDs.append(currentTrack['id'])
                 
        return recommendedTrackIDs
    
    def FilterItems(self, items: list(dict()), filter: str):
        """Leaves only those items which completely equals with the filter string

        Args:
            items (dict): Dictionary containing items
            filter (str): The string data to be equal with
        """
        # Old filter algorithm
        # table = str.maketrans(dict.fromkeys(string.punctuation + ' '))
        
        # for currentItem in items:
        #     if str(currentItem['name']).translate(table) != filter.translate(table):
        #         items.remove(currentItem)
        
        # A strict algorithm.
        # This algorithm collects the filtered items into a list, clears the original list and adds the filtered items to it
        # BECAUSE DELETING BIT BY BIT SOMEHOW STOPS AFTER 25-27 ITERATION WHYYYYYYYYYYYYYYYYYYYYYYYYYY AHHHHHHHHHHHHHHH  
        filteredItems: list(dict()) = list(dict())
          
        for currentItem in items:
            # Make the items list and filter string uppercase for ease of use
            currentItemNameUpper = str.upper(currentItem['name'])
            filterUpper = str.upper(filter)
            
            if currentItemNameUpper.startswith(filterUpper):
                filteredItems.append(currentItem)
                
        items.clear()
        items.extend(filteredItems)    
    
    def DoesGenreExists(self, genre: str):
        """Returns NotFoundError/string depending on the genre seed existence."""
        # Checking if the item string is blank
        if genre.strip():
            
            response = requests.get(
                url='https://api.spotify.com/v1/recommendations/available-genre-seeds',
                headers={
                'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
                }
            )
            
            # Checks if the token has expired
            if response.status_code == 401:
                self.auth.RefreshToken()         
                return self.DoesGenreExists(genre)         
            elif response.status_code == 200:
                
                # Checking if genre exists
                if genre in list(response.json()['genres']):
                    return f"{genre} have been successfully found.\n"   
                else:
                    raise NotFoundError(f"Unable to find {genre}.")    
        else:
            return "You have decided to leave this blank."
    
    def DoesItemExists(self, item: str, type: str, offset: int = 0):
        """Returns NotFoundError/string depending on the item seed existence."""
        # This needs to be erased from the start if we have typed more than 1 item
        self.selectedTrackID = None
        
        # Checking if the item string is blank
        if item.strip():

            # Creating query URL
            queryUrl = f"{type}%3A{item.replace(' ', '%20')}"
            # Initiaiting GET request
            response = requests.get(
                        url=f"https://api.spotify.com/v1/search?q={queryUrl}&type={type}&limit=50&offset={offset}",
                        headers={
                        "Authorization": f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
                        })    
                    
            # Checks if the token has expired (401), if not (200) then the tracks will be returned   
            if response.status_code == 401:
                self.auth.RefreshToken()         
                return self.DoesItemExists(item, type, offset=offset)         
            elif response.status_code == 200:
                responseItems = response.json()[f'{type}s']['items']

                # Filters out those items which doesn't 100% equals with the item name
                self.FilterItems(responseItems, item)
                    
                # Checks if the response has found atleast 1 item
                if len(responseItems) >= 1:
                        
                    # Creates a list with dictionaries/JSON in it which contains all
                    # the necessary infos about the tracks with same name
                    itemsWithSameName = list(dict())
                    for i in range(len(responseItems)):
                         
                        # similarlyNamedItemInfos list contains extra information about items which are in the response.
                        # Example: Typing Lady Gaga as an artist will give several results. Lady G, Lady Wei etc.
                        # That's why we need extra infos to make them easily distinguishable. 
                        similarlyNamedItemInfos = list()
                            
                        if type == 'track':    
                            for currentItem in responseItems[i]['artists']:
                                similarlyNamedItemInfos.append(currentItem['name'])
                        elif type == 'artist':
                            similarlyNamedItemInfos.append(responseItems[i]['external_urls']['spotify'])
                            
                        itemsWithSameName.append({ 
                                                    "idx" : i + 1,
                                                    "name" : responseItems[i]["name"],
                                                    "itemID" : f"{responseItems[i]['id']}",
                                                    "extra_info" : similarlyNamedItemInfos
                                                })
                     
                    # SelectCorrectTrackID will send a message which will go here
                    pub.subscribe(self.GetSelectedTrackID, 'getSelectedTrackID') 
                        
                    # Invokes/Informs/Sends data to the subscriber method (SelectCorrectTrackID method in Main.py)
                    pub.sendMessage('selectCorrectTrack', arg=itemsWithSameName, item=item, type=type, offset=offset)                  

                # Checking if we have found the 
                if self.selectedTrackID is not None:                  
                    return f"{item} {type} have been successfully found.\n", self.selectedTrackID
                else:
                    raise NotFoundError(f"Unable to find {item} {type}")                                     
        else:
            return "You have decided to leave this blank.", None
        
    # Spotify's recommendation API
    def GetRecommendations(self, seedArtists: str = None, seedGenres: str = None, seedTracks: str = None,
                           limit: int = 10, market: str = 'US', targetAcousticness: float = None,
                           targetDance: float = None, targetDurationMs: int = None,
                           targetEnergy: float = None, targetInstrumentalness: float = None,
                           targetKey: int = None, targetLiveness: float = None,
                           targetLoudness: float = None, targetMode: float = None,
                           targetPopularity: int = None, targetSpeechiness: float = None,
                           targetTempo: int = None, targetTimeSignature: int = None,
                           targetValence: float = None):
        """Calls the Recommendation API to get tracks and returns those."""
        
        response = requests.get(
            url='https://api.spotify.com/v1/recommendations',
            headers={
                'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
            },
            params={
                'seed_artists': seedArtists, 'seed_genres': seedGenres, 'seed_tracks': seedTracks,
                'limit': limit, 'market': market, 'target_acousticness': targetAcousticness,
                'target_danceability': targetDance, 'target_duration_ms': targetDurationMs,
                'target_energy': targetEnergy, 'target_instrumentalness': targetInstrumentalness,
                'target_key': targetKey, 'target_liveness': targetLiveness,
                'target_loudness': targetLoudness, 'target_mode': targetMode,
                'target_popularity': targetPopularity, 'target_speechiness': targetSpeechiness,
                'target_tempo': targetTempo, 'target_time_signature': targetTimeSignature,
                'target_valence': targetValence
            })
           
        # Checks if the token has expired (401), if not (200) then the tracks will be returned
        if response.status_code == 401:
            self.auth.RefreshToken()
            
            recommendationResult = self.GetRecommendations(seedArtists, seedGenres, seedTracks,
                                        limit, market, targetAcousticness, targetDance,
                                        targetDurationMs, targetEnergy, targetInstrumentalness, targetKey, 
                                        targetLiveness, targetLoudness, targetMode, targetPopularity,
                                        targetSpeechiness, targetTempo, targetTimeSignature, targetValence)
            
            return self.GetItemIDs(dict(recommendationResult))
        elif response.status_code == 200:
            recommendedTracksJSON = dict(response.json())
            
            # Checks if the Recommendation API didn't give tracks. If yes then it will raise an exception.
            if len(recommendedTracksJSON['tracks']) == 0:
                raise EmptyResponseOn200StatusError("\nSomehow the Recommendation algorithm didn't give tracks for you." + 
                                                    "\nTry adding more seed data to please the AI lord's tummy.")
            else:
                return self.GetItemIDs(recommendedTracksJSON)
        else:
            return response.json()