from sys import path
path.append('/home/toth-peter/Codes/Others/unknown-song-finder')

from SpotifyScripts.ClientCreatePlaylist import ConsoleCreatePlaylist


def Main():
    
    ConsoleCreatePlaylist().CreatePlaylist()

    # pub.subscribe(SelectCorrectTrackID, 'selectCorrectTrack')
    
    # # Gets recommended tracks and updates the playlist with it
    # recommendedTracks = GetRecommendedTrackIDs()  
    # PlaylistUpdate(recommendedTracks)
    
    # ssg.BeginTrackSearchAndUploading(genresToAvoid=[
    #     'ambient', 'bluegrass', 'bossanova', 'children', 'country', 'gospel',
    #     'indian', 'iranian', 'kids', 'malay', 'mandopop', 'mpb', 'opera', 'pagode',
    #     'philippines-opm', 'rainy-day', 'sertanejo', 'sleep', 'study', 'turkish'
    #     ])
        
        
if __name__ == '__main__':
    Main()