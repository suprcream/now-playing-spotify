import os
import spotipy
import time
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

sp_client_id = os.getenv('SPOTIPY_CLIENT_ID')
sp_client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
sp_direct_uri = os.getenv('SPOTIPY_REDIRECT_URI')

def update():
    try:
        # Create a new SpotifyOAuth instance for each token retrieval attempt
        sp_oauth = SpotifyOAuth(
            sp_client_id, sp_client_secret, sp_direct_uri, scope="user-read-currently-playing user-read-playback-state"
        )


        token_info = sp_oauth.get_access_token()

        if token_info:
            access_token = token_info['access_token']

            sp = spotipy.Spotify(auth=access_token)

            current_track = sp.current_playback()

            if current_track is not None and 'item' in current_track:
                track_name = current_track['item']['name']
                artist_name = current_track['item']['artists'][0]['name']

                # Update the nowplaying.txt file
                with open('nowplaying.txt', 'w') as file:
                    file.write(f"{track_name}\n-\n{artist_name}")

                print("Updated nowplaying.txt successfully.")
            else:
                print("No track is currently playing.")
    except Exception as e:
        print(f"Error: {e}")

# Main loop
try:
    while True:
        update()
        time.sleep(10)
except KeyboardInterrupt:
    print("Script terminated by user.")
