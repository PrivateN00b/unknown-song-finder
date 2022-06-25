import importlib
from Others.Exceptions.CustomExceptions import NotFoundError
from SpotifyScripts.Auth import AuthClientCredentials, AuthCode
from SpotifyScripts.PlaylistUpdater import PlayListUpdater
from SpotifyScripts.SpotifyRecommendation import SpotifyRecommendation
from SpotifyScripts.SpotifySongGatherer import SpotifySongGatherer
import keyring

inputArtists: str = ""
inputGenres: str = ""
inputTracks: str = ""

def AskForItemAndInspect(ssg: SpotifySongGatherer, sr: SpotifyRecommendation, itemName: str):
    try:
        seedItems = input(f"Add X {itemName}(s)'s names if you wish: ")
        if itemName == 'genre':
            print(sr.DoesGenreExists(genre=seedItems))
            return seedItems
        else:
            output, itemID = sr.DoesItemExists(item=seedItems, type=itemName)
            print(output)
            return itemID
    except NotFoundError as e:
        print(e)
        AskForItemAndInspect(ssg, sr, itemName)

def RecommendationAPI(ssg: SpotifySongGatherer, sr: SpotifyRecommendation):
    """This function deals with calling the official Spotify Recommandation API"""
    
    
    print("""Add maximum of 5 data in any combination of artists, genres or tracks:
            IMPORTANT: Insert ID's and not the name of the artists and tracks.
            To add more than 1 information, separate them by using the (,) separator.
            If you want to avoid filling artists, genres or tracks then leave that part(s) blank by pressing ENTER.
          """)
    global inputArtists, inputGenres, inputTracks
    inputArtists = AskForItemAndInspect(ssg, sr, 'artist')
    inputGenres = AskForItemAndInspect(ssg, sr, 'genre')
    inputTracks = AskForItemAndInspect(ssg, sr, 'track')
        
    recommendationResult = sr.GetRecommendations(seedArtists=inputArtists, seedGenres=inputGenres,
                                                 seedTracks=inputTracks, limit=30)
    return list(recommendationResult)

def PlaylistUpdate(pu: PlayListUpdater, tracks: list):
    name = "Recommendation API Tracks"
    description = "Tracks based on "
    
    # Fills out the description variable.
    if inputArtists != "": description += f"{inputArtists} artist(s), " 
    if inputGenres != "": description += f"{inputGenres} genre(s), " 
    if inputTracks != "": description += f"{inputTracks} track(s)." 
    
    # Returns playlistID or None
    playlistID = pu.DoesPlayListExists(name, description)
    
    #Creating Playlist and checking if it already exists
    if playlistID is None:
        pu.CreatePlaylist(name, description)
    else:
        print("Playlist already exists!")
    
    #Adding songs
    pu.AddToPlaylist(playlistID, tracks)
    
    print("Successful!")

def Main():
    ssg = SpotifySongGatherer(AuthClientCredentials())
    sr = SpotifyRecommendation(AuthCode())
    pu = PlayListUpdater(AuthCode())
    
    recommendedTracks = RecommendationAPI(ssg, sr)
    
    PlaylistUpdate(pu, recommendedTracks)
    
    # ssg.BeginTrackSearchAndUploading(genresToAvoid=[
    #     'ambient', 'bluegrass', 'bossanova', 'children', 'country', 'gospel',
    #     'indian', 'iranian', 'kids', 'malay', 'mandopop', 'mpb', 'opera', 'pagode',
    #     'philippines-opm', 'rainy-day', 'sertanejo', 'sleep', 'study', 'turkish'
    #     ])
        
        
if __name__ == '__main__':
    Main()