import pytest
from SpotifyScripts.Auth import AuthClientCredentials
from SpotifyScripts.SpotifySongGatherer import SpotifySongGatherer

class TestSpotifySongGatherer():
    
    def test_search_tracks_success(self):
        # ARRANGE
        ssg = SpotifySongGatherer(AuthClientCredentials())
        # ACT
        result = ssg.SearchTracks(q="year:1969", tp=['track'], market='US', offset=0, limit=1)
        # ASSERT
        assert result.status_code == 200
        
    @pytest.mark.parametrize("ids", ['6BOOnwbQFco9AV0rKXZ8VV', '6BOOnwbQFco9AV0rKXZ8VV,4CqAtoRg4JGaP8fgl5kGO3', ''])
    def test_get_tracks_audio_features_one_two_blank_IDs(self, ids):
        # ARRANGE
        ssg = SpotifySongGatherer(AuthClientCredentials())
        # ACT
        result = ssg.GetTracksAudioFeatures(ids=ids)
        # ASSERT
        assert result.status_code == 200
        
    def test_get_avalaible_genre_seeds_success(self):
        # ARRANGE
        ssg = SpotifySongGatherer(AuthClientCredentials())
        # ACT
        result = ssg.GetAvalaibleGenreSeeds()
        # ASSERT
        assert result.status_code == 200
        
    def AddToCSV(self, tracksToAdd, tracksAudioFeatures):
        # ARRANGE
        ssg = SpotifySongGatherer(AuthClientCredentials())
        # ACT
        result = ssg.AddToCSV(tracksToAdd, tracksAudioFeatures)
        # ASSERT
        assert result == 69