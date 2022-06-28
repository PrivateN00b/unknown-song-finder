from Others.Exceptions.CustomExceptions import *
from SpotifyScripts.Auth import AuthClientCredentials, AuthCode
from SpotifyScripts.PlaylistUpdater import PlayListUpdater
from SpotifyScripts.SpotifyRecommendation import SpotifyRecommendation
from SpotifyScripts.SpotifySongGatherer import SpotifySongGatherer

inputArtists: str = ""
inputGenres: str = ""
inputTracks: str = ""

def AskForItemAndInspect(ssg: SpotifySongGatherer, sr: SpotifyRecommendation, itemName: str):
    """Checks if the requested name exists in the Spotify database.

    Args:
        ssg (SpotifySongGatherer): SpotifySongGatherer class
        sr (SpotifyRecommendation): SpotifyRecommendation class
        itemName (str): The name to check it's existence

    Returns:
        if itemName exists: The corresponding ID or genre name.
        if itemName doesn't: Void
    """
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
    """This function deals with calling the official Spotify Recommandation API.
    
    Args:
        ssg (SpotifySongGatherer): SpotifySongGatherer class
        sr (SpotifyRecommendation): SpotifyRecommendation class

    Returns: A list with recommended trackID's by the algorithm.
    """ 
    # Asks for artist/genre/track names and checks if they exist or not
    print("""Add maximum of 5 data in any combination of artists, genres or tracks:
            To add more than 1 information, separate them by using the (,) separator.
            If you want to avoid filling artists, genres or tracks then leave that part(s) blank by pressing ENTER.
          """)
    global inputArtists, inputGenres, inputTracks
    inputArtists = AskForItemAndInspect(ssg, sr, 'artist')
    inputGenres = AskForItemAndInspect(ssg, sr, 'genre')
    inputTracks = AskForItemAndInspect(ssg, sr, 'track')
    
    # Gets the recommended trackID's which the API suggests
    recommendationResult = sr.GetRecommendations(seedArtists=inputArtists, seedGenres=inputGenres,
                                                 seedTracks=inputTracks, limit=30)
    return list(recommendationResult)

def PlaylistUpdate(pu: PlayListUpdater, tracks: list):
    """Creates a playlist or updates it with tracks.

    Args:
        pu (PlayListUpdater): PlayListUpdater class
        tracks (list): A list containing trackID's
    """
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
    # Defining and initializing classes
    ssg = SpotifySongGatherer(AuthClientCredentials())
    sr = SpotifyRecommendation(AuthCode())
    pu = PlayListUpdater(AuthCode())
    
    # Gets trackID's
    recommendedTracks = RecommendationAPI(ssg, sr)
    
    # Updates playlist with the previously gotten trackID's
    PlaylistUpdate(pu, recommendedTracks)
    
    # ssg.BeginTrackSearchAndUploading(genresToAvoid=[
    #     'ambient', 'bluegrass', 'bossanova', 'children', 'country', 'gospel',
    #     'indian', 'iranian', 'kids', 'malay', 'mandopop', 'mpb', 'opera', 'pagode',
    #     'philippines-opm', 'rainy-day', 'sertanejo', 'sleep', 'study', 'turkish'
    #     ])
        
        
if __name__ == '__main__':
    Main()