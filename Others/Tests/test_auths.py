from SpotifyScripts.Auth import AuthClientCredentials, AuthCode

class TestAuthClientCredentials():

    def test_authorize(self) -> None:
        # ARRANGE
        authorize = AuthClientCredentials()
        # ACT
        authorize.Authorize()
        # ASSERT
        assert authorize.token is not None
        
    def test_refresh_token(self) -> None:
        # ARRANGE
        authorize = AuthClientCredentials()
        # ACT
        authorize.Authorize()
        oldToken = authorize.token
        authorize.RefreshToken()
        # ASSERT
        assert authorize.token['access_token'] != oldToken['access_token']

class TestAuthCode():
    
    def test_authorize(self) -> None:
        # ARRANGE
        authorize = AuthCode()
        # ACT
        authorize.Authorize()
        # ASSERT
        assert authorize.token is not None
        
    def test_refresh_token(self) -> None:
        # ARRANGE
        authorize = AuthCode()
        # ACT
        authorize.Authorize()
        oldToken = authorize.token
        authorize.RefreshToken()
        # ASSERT
        assert authorize.token['access_token'] != oldToken['access_token']