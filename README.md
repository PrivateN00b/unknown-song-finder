# spotify-playlist-recommender
This script runs Spotify's recommendation API which assembles several playlists, like Discover Weekly (favorite feature for me). 

If you run out of the 30 new songs from the Weekly, you could perhaps rerun it by adding maximum 5 infos (artist, genre, song) to this script.

The script uses Client Credentials Flow.

# How to use
Download one of the executable files and run it.

1. Add permission for the script to access your profile
2. Add artists, genres, tracks by including the names and press enter. 
    - If you add multiple tracks for example, just separate each track with a semicolon
    - You can omit / leave sections blank. Just press enter
    - Do know that the sum of these can be MAX 5 infos

Examples:
'''
Add X artist(s)'s names if you wish: Auroveoir.
...
Add X genre(s)'s names if you wish: rock
...
Add X track(s)'s names if you wish: Imbolygó
'''

'''
Add X artist(s)'s names if you wish:
...
Add X genre(s)'s names if you wish:
...
Add X track(s)'s names if you wish: Pretty and Depressed, SEISHUN WO KIRISAKU HADO, Untouchable
'''

# TODO:
- Refactoring
- GUI app?
- Maybe a homemade recommendation AI?
- Touching grass