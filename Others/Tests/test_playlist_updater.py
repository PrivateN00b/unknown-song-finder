import json
from SpotifyScripts.Auth import AuthCode
from SpotifyScripts.PlaylistUpdater import PlayListUpdater

class TestPlaylistUpdater():
        
    def test_get_current_user_id(self):
        # ARRANGE
        playListUpdater = PlayListUpdater(AuthCode())
        # ACT     
        result = playListUpdater.GetCurrentUserID()
        # ASSERT
        assert len(result) > 0
        
    def test_get_existing_playlists(self):
        # ARRANGE
        playListUpdater = PlayListUpdater(AuthCode())
        # ACT     
        result = playListUpdater.GetExistingPlaylists()
        # ASSERT
        assert result.status_code == 200