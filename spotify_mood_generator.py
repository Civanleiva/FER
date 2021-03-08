from os import name
import spotipy
import random
import webbrowser

client_id = ''
client_secret = ''
redirect_uri = 'http://127.0.0.1:8080/callback'
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
username = ''

token = spotipy.util.prompt_for_user_token(
    username, scope, client_id, client_secret, redirect_uri)


def generatePlaylist(mood, stringMood):
    if token:
        sp = spotipy.Spotify(auth=token)
        print("Token created")

        top_artists_names = []
        top_artists_uri = []

        ranges = ['short_term', 'medium_term', 'long_term']
        for r in ranges:
            top_artists_all_data = sp.current_user_top_artists(
                limit=500, time_range=r)
            top_artist_data = top_artists_all_data['items']

            for artist_data in top_artist_data:
                if artist_data['name'] not in top_artists_names:
                    top_artists_names.append(artist_data['name'])
                    top_artists_uri.append(artist_data['uri'])

        followed_artists_all_data = sp.current_user_followed_artists(limit=50)
        followed_arists_data = (followed_artists_all_data['artists'])

        for artist_data in followed_arists_data["items"]:
            if artist_data['name'] not in top_artists_names:
                top_artists_names.append(artist_data['name'])
                top_artists_uri.append(artist_data['uri'])
        print("Artist information found")

        top_tracks_uri = []
        for artist in top_artists_uri:
            top_tracks_all_data = sp.artist_top_tracks(artist)
            top_tracks_data = top_tracks_all_data['tracks']

            for track_data in top_tracks_data:
                top_tracks_uri.append(track_data['uri'])
        print("Artist top tracks found")

        selected_tracks_uri = []

        random.shuffle(top_tracks_uri)

        def group(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        for tracks in list(group(top_tracks_uri, 50)):
            tracks_all_data = sp.audio_features(tracks)
            for track_data in tracks_all_data:
                try:
                    if mood < 0.10:
                        if (0 <= track_data["valence"] <= (mood + 0.15)
                            and track_data["danceability"] >= (mood * 8)
                                and track_data["energy"] <= (mood * 10)):
                            selected_tracks_uri.append(track_data["uri"])
                    elif 0.1 <= mood <= 0.25:
                        if ((mood - 0.075) <= track_data["valence"] <= (mood + 0.075)
                            and track_data["danceability"] <= (mood * 4)
                                and track_data["energy"] <= (mood * 5)):
                            selected_tracks_uri.append(track_data["uri"])
                    elif 0.25 <= mood <= 0.5:
                        if ((mood - 0.05) <= track_data["valence"] <= (mood + 0.05)
                            and track_data["danceability"] <= (mood * 1.75)
                                and track_data["energy"] <= (mood * 1.75)):
                            selected_tracks_uri.append(track_data["uri"])
                    elif 0.50 <= mood < 0.75:
                        if ((mood - 0.075) <= track_data["valence"] <= (mood + 0.075)
                            and track_data["danceability"] >= (mood/2.5)
                                and track_data["energy"] >= (mood/2)):
                            selected_tracks_uri.append(track_data["uri"])
                    elif 0.75 <= mood < 0.90:
                        if ((mood - 0.075) <= track_data["valence"] <= (mood + 0.075)
                            and track_data["danceability"] >= (mood/2)
                                and track_data["energy"] >= (mood/1.75)):
                            selected_tracks_uri.append(track_data["uri"])
                    elif mood >= 0.9:
                        if ((mood - 0.15) <= track_data["valence"] <= 1
                            and track_data["danceability"] >= (mood / 1.75)
                                and track_data["energy"] >= (mood / 1.5)):
                            selected_tracks_uri.append(track_data["uri"])
                except TypeError as te:
                    continue
        print("Songs according to mood found")

        user_all_data = sp.current_user()
        user_id = user_all_data["id"]

        playlist_all_data = sp.user_playlist_create(user_id, stringMood)
        print("Playlist created")
        playlist_id = playlist_all_data["id"]
        print("Playlist ID found")
        random.shuffle(selected_tracks_uri)
        print("Tracks shuffled")
        sp.user_playlist_add_tracks(
            user_id, playlist_id, selected_tracks_uri[0:30])
        print("Tracks added")
        webbrowser.open(playlist_all_data["url"], new=2)