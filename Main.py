import importlib
from Auth import AuthClientCredentials, AuthCode
from Others.Exceptions.CustomExceptions import NotFoundError
from SpotifyRecommendation import SpotifyRecommendation
from SpotifySongGatherer import SpotifySongGatherer
import keyring

def AskForItemAndInspect(ssg: SpotifySongGatherer, sr: SpotifyRecommendation, itemName: str):
    try:
        seedItems = input(f"Add X {itemName}(s)'s name if you wish: ")
        if itemName == 'genre':
            print(sr.DoesGenreExists(genre=seedItems))
        else:
            print(sr.DoesItemExists(item=seedItems, type=itemName)) 
    except NotFoundError as e:
        print(e)
        AskForItemAndInspect(ssg, sr, itemName)

def RecommendationAPI(ssg: SpotifySongGatherer, sr: SpotifyRecommendation):
    """This function deals with calling the official Spotify Recommandation API"""
    
    
    print("""Add maximum of 5 data in any combination of artists, genres or tracks:

            For adding more than 1 information, separate them by using the (,) separator.
            If you want to avoid filling artists, genres or tracks then leave that part(s) blank by pressing ENTER.
          """)
    AskForItemAndInspect(ssg, sr, 'artist')
    AskForItemAndInspect(ssg, sr, 'genre')
    AskForItemAndInspect(ssg, sr, 'track')
        
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