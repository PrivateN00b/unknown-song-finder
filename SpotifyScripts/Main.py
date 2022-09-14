from Others.Exceptions.CustomExceptions import *
from SpotifyScripts.Auth import AuthClientCredentials, AuthCode
from SpotifyScripts.PlaylistUpdater import PlayListUpdater
from SpotifyScripts.SpotifyRecommendation import SpotifyRecommendation
from SpotifyScripts.SpotifySongGatherer import SpotifySongGatherer
from SpotifyScripts.ClientCreatePlaylist import *
from pubsub import pub

def Main():
    
    ConsoleCreatePlaylist()

    # pub.subscribe(SelectCorrectTrackID, 'selectCorrectTrack')
    
    # # Gets recommended tracks and updates the playlist with it
    # recommendedTracks = GetRecommendedTrackIDs()  
    # PlaylistUpdate(recommendedTracks)
    
    # ssg.BeginTrackSearchAndUploading(genresToAvoid=[
    #     'ambient', 'bluegrass', 'bossanova', 'children', 'country', 'gospel',
    #     'indian', 'iranian', 'kids', 'malay', 'mandopop', 'mpb', 'opera', 'pagode',
    #     'philippines-opm', 'rainy-day', 'sertanejo', 'sleep', 'study', 'turkish'
    #     ])
        
        
# if __name__ == '__main__':
#     Main()