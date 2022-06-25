import importlib
from Auth import AuthClientCredentials, AuthCode
from SpotifyRecommendation import SpotifyRecommendation
from SpotifySongGatherer import SpotifySongGatherer
import keyring


def RecommendationAPI(ssg: SpotifySongGatherer, sr: SpotifyRecommendation):
    """This function deals with calling the official Spotify Recommandation API"""
    
    
    print("""Add maximum of 5 data in any combination of artists, genres or tracks:

            For adding more than 1 information, separate them by using the (,) separator.
            If you want to avoid filling artists, genres or tracks then leave that part(s) blank by pressing ENTER.
          """)
    seedArtists = input("Add X artist(s)'s name if you wish: ")
    print(sr.DoesItemExists(item=seedArtists, type='artist'))
    seedGenres = input("Add X genre(s)'s name if you wish: ")
    print(sr.DoesGenreExists(genre=seedGenres))
    seedTracks = input("Add X track(s)'s name if you wish: ")
    print(sr.DoesItemExists(item=seedTracks, type='track'))
        
    recommendationResult = sr.GetRecommendations(seedArtists="7cvljqLNhWNFMb8wP2NImJ",
                                                 seedTracks="4n0sVfRnd0UJsqcbPj7GqN,7py4CtNzC4SN0z0CaMONYM",
                                                 limit=10)
    print(recommendationResult)

def Main():
    ssg = SpotifySongGatherer(AuthClientCredentials())
    sr = SpotifyRecommendation(AuthCode())
    RecommendationAPI(ssg, sr)
    
    # ssg.BeginTrackSearchAndUploading(genresToAvoid=[
    #     'ambient', 'bluegrass', 'bossanova', 'children', 'country', 'gospel',
    #     'indian', 'iranian', 'kids', 'malay', 'mandopop', 'mpb', 'opera', 'pagode',
    #     'philippines-opm', 'rainy-day', 'sertanejo', 'sleep', 'study', 'turkish'
    #     ])
        
        
if __name__ == '__main__':
    Main()