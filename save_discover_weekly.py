import argparse
import datetime
from functools import cached_property

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class PlaylistNotFoundError(Exception):
    pass


class Spotify(spotipy.Spotify):
    def __init__(self, playlist_name=None):
        self.playlist_name = playlist_name
        scope = "playlist-modify-private playlist-read-private playlist-modify-public"
        super().__init__(
            auth_manager=SpotifyOAuth(
                scope=scope,
            )
        )

    def create_discover_weekly_playlist(self):
        if self.discover_weekly_id:
            new_playlist = self.create_playlist(
                self.playlist_name or f"{self.start_of_week} Re-Discover Weekly"
            )
            if self.playlist_name:
                existing_tracks = self.get_track_ids_from_playlist(new_playlist["id"])
                new_tracks = list(
                    self.discover_weekly_tracks.difference(existing_tracks)
                )
                if new_tracks:
                    self.playlist_add_items(new_playlist["id"], new_tracks)
            else:
                self.playlist_replace_items(
                    new_playlist["id"],
                    [track_id for track_id in self.discover_weekly_tracks],
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

    @property
    def discover_weekly_tracks(self):
        return self.get_track_ids_from_playlist(self.discover_weekly_id)

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

    def get_track_ids_from_playlist(self, playlist_id):
        track_ids = set()
        
        offset = 0
        while True:
            tracks = self.playlist_tracks(playlist_id, offset=offset)
            for track in tracks["items"]:
                track_ids.add(track["track"]["id"])
            if tracks["next"] is not None:
                offset += 100
            else:
                break
        
        return track_ids

    @property
    def start_of_week(self):
        now = datetime.datetime.now()
        monday = now - datetime.timedelta(days=now.weekday())
        return monday.strftime("%B %d '%y")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PLAYLIST_NAME]",
        description="Set name of playlist to add to or use default"
    )
    parser.add_argument(
        "-pn", "--playlist_name", default=None
    )
    args = parser.parse_args()
    spotify = Spotify(args.playlist_name)
    spotify.create_discover_weekly_playlist()
