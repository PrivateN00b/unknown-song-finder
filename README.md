# unknown-song-finder
It's not 100% finished yet since it just uses Implicit Grant Flow, and I don't have a home server running to make this run weekly.

#How to get the token to make the script work
Just go to this site and request a token: https://developer.spotify.com/console/post-playlist-tracks/?playlist_id=&position=&uris= and add change the current token string.

You can change the amount of songs to add and popularity thresholds on line 63 (SongFinder(token, 0, 80, 30)).
  SongFinder(token, minPopularity, maxPopularity, amountOfSongsToAdd)
