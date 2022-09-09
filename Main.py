from Others.Exceptions.CustomExceptions import *
from SpotifyScripts.Auth import AuthClientCredentials, AuthCode
from SpotifyScripts.PlaylistUpdater import PlayListUpdater
from SpotifyScripts.SpotifyRecommendation import SpotifyRecommendation
from SpotifyScripts.SpotifySongGatherer import SpotifySongGatherer
from pubsub import pub

# Defining and initializing global classes/attributes
ssg = SpotifySongGatherer(AuthClientCredentials())
sr = SpotifyRecommendation(AuthCode())
pu = PlayListUpdater(AuthCode())

inputArtists: str = ""
inputGenres: str = ""
inputTracks: str = ""

def SelectCorrectTrackID(arg: list(dict()), item: str, type: str, offset: int):
    """Makes the user to choose a track out of the found ones with the same names.
    
    Returns: Selected track's ID
    """    
    for currentTrack in arg:
        print(f"Number: {currentTrack['idx']}, Name: {currentTrack['name']}, Info: {currentTrack['extra_info']}")
    
    print("""
        The algorithm have found numerous tracks with the same name.
          Navigation options (things you can write in):
          'back' key: List the previous song options
          'next' or any type of input key: List the next song options
          """)
    
    # This will try to convert the input into -1. If you didn't write -1, for example an ENTER then it will catch it and convert to -1
    selectedNum = input("Select the correct track by inserting the corresponding number: ")
    try:
        selectedNum = int(selectedNum)
    except ValueError:
        print('') # This is just a placeholder.
    
    # Checks if the user responded with -1. (If the algorithm included the correct track in the list)
    if isinstance(selectedNum, int):        
        print("-"*20+"\n")
        
        # Sends back the selected track's ID to DoesItemExists for returning the ID
        pub.sendMessage('getSelectedTrackID', selectedID=arg[selectedNum - 1]['itemID'])
    elif selectedNum == 'back' and offset >= 50:
        print("Checking the previous list...\n")
        pub.sendMessage('rerunCorrectTrackSearch', item=item, type=type, offset=(offset-50))
    elif selectedNum == 'back' and offset < 50:
        print("There is no previous list to check into!\n")
    else:
        print("Checking the next list...\n")
        pub.sendMessage('rerunCorrectTrackSearch', item=item, type=type, offset=(offset+50))
        
        

def AskForItemAndInspect(itemName: str) -> list:
    """Checks if the requested name exists in the Spotify database.

    Args:
        itemName (str): The name to check it's existence

    Returns:
        if itemName exists: The corresponding ID or genre name.
        if itemName doesn't: Void
    """
    global inputArtists, inputGenres, inputTracks, ssg, sr
    
    try:
        seedItems = input(f"Add X {itemName}(s)'s names if you wish: ")
        if itemName == 'genre':
            print(sr.DoesGenreExists(genre=seedItems))
            inputGenres = seedItems # This is needed for the playlist's description
            return seedItems
        else:
            allItemIDs = list()
            for currentItem in seedItems.split(','):
                currentItem = currentItem.strip()
                output, itemID = sr.DoesItemExists(item=currentItem, type=itemName)
                print(output)
                allItemIDs.append(itemID)
             
            # This is needed for the playlist's description    
            if itemName == 'artist':
                inputArtists = seedItems
            else:
                inputTracks = seedItems
                
            return allItemIDs
    except NotFoundError as e:
        print(e)
        AskForItemAndInspect(itemName)

def RecommendationAPI():
    """This function deals with calling the official Spotify Recommandation API.

    Returns: A list with recommended trackID's by the algorithm.
    """ 
    global ssg, sr
    
    # Asks for artist/genre/track names and checks if they exist or not
    print("""Add maximum of 5 data in any combination of artists, genres or tracks:
            To add more than 1 information, separate them by using the (,) separator.
            If you want to avoid filling artists, genres or tracks then leave that part(s) blank by pressing ENTER.
          """)
    inputArtistIDs = AskForItemAndInspect('artist')
    inputGenres = AskForItemAndInspect('genre')
    inputTrackIDs = AskForItemAndInspect('track')
    
    # Gets the recommended trackID's which the API suggests
    recommendationResult = sr.GetRecommendations(seedArtists=inputArtistIDs, seedGenres=inputGenres,
                                                 seedTracks=inputTrackIDs, limit=30)
    return list(recommendationResult)

def PlaylistUpdate(tracks: list):
    """Creates a playlist or updates it with tracks.

    Args:
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
        playlistID = pu.DoesPlayListExists(name)
    else:
        pu.ChangePlaylistDetails(name, description)
        
    
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
    
    pub.subscribe(SelectCorrectTrackID, 'selectCorrectTrack')
    
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