import datetime
from functools import cached_property

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class PlaylistNotFoundError(Exception):
    pass


class Spotify(spotipy.Spotify):
    def __init__(self):
        scope = "playlist-modify-private playlist-read-private"
        super().__init__(
            auth_manager=SpotifyOAuth(
                scope=scope,
            )
        )

    def create_discover_weekly_playlist(self):
        if self.discover_weekly_id:
            new_playlist = self.create_playlist(
                f"{self.start_of_week} Re-Discover Weekly"
            )
            self.playlist_replace_items(
                new_playlist["id"],
                [track["track"]["id"] for track in self.discover_weekly_tracks],
            )

    def create_playlist(self, playlist_name):
        try:
            return self.find_playlist(playlist_name)
        except PlaylistNotFoundError:
            return self.user_playlist_create(
                self.current_user()["id"], playlist_name, public=False
            )

    @cached_property
    def discover_weekly_id(self):
        discover_weekly_playlist = self.find_playlist("Discover Weekly")
        return discover_weekly_playlist["id"]

    @cached_property
    def discover_weekly_tracks(self):
        return self.playlist_tracks(self.discover_weekly_id)["items"]

    def find_playlist(self, playlist_name):
        offset = 0
        while True:
            playlists = self.current_user_playlists(offset=offset).get("items")
            if not playlists:
                raise PlaylistNotFoundError(f"playlist not found {playlist_name}")
            for playlist in playlists:
                if playlist["name"] == playlist_name:
                    return playlist
            offset += 50

    @property
    def start_of_week(self):
        now = datetime.datetime.now()
        monday = now - datetime.timedelta(days=now.weekday())
        return monday.strftime("%B %d '%y")


if __name__ == "__main__":
    spotify = Spotify()
    spotify.create_discover_weekly_playlist()
