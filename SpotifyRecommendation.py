import requests
from Auth import Auth

class SpotifyRecommendation:
    
    auth: Auth = None
    
    def __init__(self, auth: Auth):
        self.auth = auth
        self.auth.Authorize()
    
    def GetTrackIDs(self, data: dict):
        """Selects the IDs from the dictionary JSON object and returns it."""
        recommendedTrackIDs = list()
        for currentTrack in data['tracks']:
            recommendedTrackIDs.append(currentTrack['id'])
                 
        return recommendedTrackIDs
    
    def DoesGenreExists(self, genre: str):
        """Returns if the genre seed exists."""
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
        else:
            xd = response.json()
            if genre in response.json()['genres']:
                return True
            else:
                return False 
    
    def DoesItemExists(self, item: str, type: str):
        # Creating query URL
        queryUrl = f"?q=artist%3A{item.replace(' ', '+')}&type={type}"
        # Initiaiting GET request
        response = requests.get(
                    url=f"https://api.spotify.com/v1/search{queryUrl}",
                    headers={
                    "Authorization": f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
                    })    
        
        # Checks if the token has expired
        if response.status_code == 401:
            self.auth.RefreshToken()         
            return self.DoesItemExists(item, type)         
        else:
            xd = response.json()
            if len(response.json()[f'{type}s']['items']) >= 1:
                return True
            else:
                return False          
    
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
           
        # Checks if the token has expired
        if response.status_code == 401:
            self.auth.RefreshToken()
            
            recommendationResult = self.GetRecommendations(seedArtists, seedGenres, seedTracks,
                                        limit, market, targetAcousticness, targetDance,
                                        targetDurationMs, targetEnergy, targetInstrumentalness, targetKey, 
                                        targetLiveness, targetLoudness, targetMode, targetPopularity,
                                        targetSpeechiness, targetTempo, targetTimeSignature, targetValence)
            
            return self.GetTrackIDs(dict(recommendationResult))
        else:
            return response.json()