from Others.Exceptions.CustomExceptions import *
from SpotifyScripts.Auth import AuthClientCredentials, AuthCode
from SpotifyScripts.PlaylistUpdater import PlayListUpdater
from SpotifyScripts.SpotifyRecommendation import SpotifyRecommendation
from SpotifyScripts.SpotifySongGatherer import SpotifySongGatherer

# Defining and initializing global classes/attributes
ssg = SpotifySongGatherer(AuthClientCredentials())
sr = SpotifyRecommendation(AuthCode())
pu = PlayListUpdater(AuthCode())

inputArtists: str = ""
inputGenres: str = ""
inputTracks: str = ""

def AskForItemAndInspect(itemName: str):
    """Checks if the requested name exists in the Spotify database.

    Args:
        ssg (SpotifySongGatherer): SpotifySongGatherer class
        sr (SpotifyRecommendation): SpotifyRecommendation class
        itemName (str): The name to check it's existence

    Returns:
        if itemName exists: The corresponding ID or genre name.
        if itemName doesn't: Void
    """
    global ssg, sr
    
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
        AskForItemAndInspect(itemName)

def RecommendationAPI():
    """This function deals with calling the official Spotify Recommandation API.
    
    Args:
        ssg (SpotifySongGatherer): SpotifySongGatherer class
        sr (SpotifyRecommendation): SpotifyRecommendation class

    Returns: A list with recommended trackID's by the algorithm.
    """ 
    global inputArtists, inputGenres, inputTracks, ssg, sr
    
    # Asks for artist/genre/track names and checks if they exist or not
    print("""Add maximum of 5 data in any combination of artists, genres or tracks:
            To add more than 1 information, separate them by using the (,) separator.
            If you want to avoid filling artists, genres or tracks then leave that part(s) blank by pressing ENTER.
          """)
    inputArtists = AskForItemAndInspect('artist')
    inputGenres = AskForItemAndInspect('genre')
    inputTracks = AskForItemAndInspect('track')
    
    # Gets the recommended trackID's which the API suggests
    recommendationResult = sr.GetRecommendations(seedArtists=inputArtists, seedGenres=inputGenres,
                                                 seedTracks=inputTracks, limit=30)
    return list(recommendationResult)

def PlaylistUpdate(tracks: list):
    """Creates a playlist or updates it with tracks.

    Args:
        pu (PlayListUpdater): PlayListUpdater class
        tracks (list): A list containing trackID's
    """
    global inputArtists, inputGenres, inputTracks, pu
    
    name = "Recommendation API Tracks"
    description = "Tracks based on "
    
    # Fills out the description variable.
    if inputArtists != "": description += f"{inputArtists} artist(s), " 
    if inputGenres != "": description += f"{inputGenres} genre(s), " 
    if inputTracks != "": description += f"{inputTracks} track(s)." 
    
    # Returns playlistID or None
    playlistID = pu.DoesPlayListExists(name)
    
    #Creating Playlist and checking if it already exists
    if playlistID is None:
        pu.CreatePlaylist(name, description)
    else:
        print("Playlist already exists!")
    
    #Adding songs
    pu.AddToPlaylist(playlistID, tracks)
    
    print("Successful!")

def GetRecommendedTrackIDs():
    """Gets the recommended trackIDs from the Recommendation API
    
    Returns: dictionary containing trackIDs
    """
    try:
        recommendedTracks = RecommendationAPI()
  
        return recommendedTracks
    except EmptyResponseOn200StatusError as e:
        print(e)
        
        # Asking for seed datas again
        GetRecommendedTrackIDs()
        
    
def Main():
    
    # Gets recommended tracks and updates the playlist with it
    recommendedTracks = GetRecommendedTrackIDs()  
    PlaylistUpdate(recommendedTracks)
    
    # ssg.BeginTrackSearchAndUploading(genresToAvoid=[
    #     'ambient', 'bluegrass', 'bossanova', 'children', 'country', 'gospel',
    #     'indian', 'iranian', 'kids', 'malay', 'mandopop', 'mpb', 'opera', 'pagode',
    #     'philippines-opm', 'rainy-day', 'sertanejo', 'sleep', 'study', 'turkish'
    #     ])
        
        
if __name__ == '__main__':
    Main()