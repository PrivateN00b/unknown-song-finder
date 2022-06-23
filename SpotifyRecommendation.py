from tkinter.messagebox import NO
import requests
from Auth import Auth

class SpotifyRecommendation:
    
    auth: Auth = None
    
    def __init__(self, auth: Auth):
        self.auth = auth
        self.auth.Authorize()
    
    # Spotify's recommendation API
    def GetRecommendations(self, seedArtists: str, seedGenres: str, seedTracks: str,
                           limit: int = None, market: str = 'US', maxAcousticness: float = None,
                           maxDance: float = None, maxDurationMs: int = None,
                           maxEnergy: float = None, maxInstrumentalness: float = None,
                           maxKey: int = None, maxLiveness: float = None,
                           maxLoudness: float = None, maxMode: float = None,
                           maxPopularity: int = None, maxSpeechiness: float = None,
                           maxTempo: int = None, maxTimeSignature: int = None,
                           maxValence: float = None, minAcousticness: float = None,
                           minDance: float = None, minDurationMs: int = None,
                           minEnergy: float = None, minInstrumentalness: float = None,
                           minKey: int = None, minLiveness: float = None,
                           minLoudness: float = None, minMode: float = None,
                           minPopularity: int = None, minSpeechiness: float = None,
                           minTempo: int = None, minTimeSignature: int = None,
                           minValence: float = None, targetAcousticness: float = None,
                           targetDance: float = None, targetDurationMs: int = None,
                           targetEnergy: float = None, targetInstrumentalness: float = None,
                           targetKey: int = 6, targetLiveness: float = None,
                           targetLoudness: float = None, targetMode: float = None,
                           targetPopularity: int = None, targetSpeechiness: float = None,
                           targetTempo: int = None, targetTimeSignature: int = None,
                           targetValence: float = None
                           ):
        response = requests.get(
        url='https://api.spotify.com/v1/recommendations',
        headers={
            'Authorization': f"{self.auth.token['token_type']} {self.auth.token['access_token']}"
        },
        params={
            'seed_artists': seedArtists,
            'seed_genres': seedGenres,
            'seed_tracks': seedTracks
        })
        return response.json()