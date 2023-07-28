import argparse
import datetime
from collections.abc import KeysView
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, Union

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class PlaylistNotFoundError(Exception):
    pass


@dataclass
class Playlist:
    name: str
    id: str


class Spotify(spotipy.Spotify):
    def __init__(self, playlist_name: Union[str, None] = None):
        self.playlist_name = playlist_name
        scope = "playlist-modify-private playlist-read-private playlist-modify-public"
        super().__init__(
            auth_manager=SpotifyOAuth(
                scope=scope,
            )
        )

    def create_discover_weekly_playlist(self) -> None:
        if self.discover_weekly_id:
            new_playlist = self.create_playlist(
                self.playlist_name or f"{self.start_of_week} Re-Discover Weekly"
            )
            if self.playlist_name:
                existing_tracks = self.get_track_ids_from_playlist(new_playlist.id)
                new_tracks = [
                    track_id
                    for track_id in self.discover_weekly_tracks
                    if track_id not in existing_tracks
                ]
                if new_tracks:
                    self.playlist_add_items(new_playlist.id, new_tracks)
            else:
                self.playlist_replace_items(
                    new_playlist.id,
                    [track_id for track_id in self.discover_weekly_tracks],
                )
        raise Exception("Could not find discover weekly playlist")

    def create_playlist(self, playlist_name: str) -> Playlist:
        try:
            return self.find_playlist(playlist_name)
        except PlaylistNotFoundError:
            created_playlist = self.user_playlist_create(
                self.current_user()["id"], playlist_name, public=False
            )
            return Playlist(name=created_playlist["name"], id=created_playlist["id"])

    @cached_property
    def discover_weekly_id(self) -> str:
        discover_weekly_playlist = self.find_playlist("Discover Weekly")
        return discover_weekly_playlist.id

    @property
    def discover_weekly_tracks(self) -> KeysView:
        return self.get_track_ids_from_playlist(self.discover_weekly_id)

    def find_playlist(self, playlist_name: str) -> Playlist:
        offset = 0
        while True:
            playlists = self.current_user_playlists(offset=offset).get("items")
            if not playlists:
                raise PlaylistNotFoundError(f"playlist not found {playlist_name}")
            for playlist in playlists:
                if playlist["name"] == playlist_name:
                    return Playlist(name=playlist["name"], id=playlist["id"])
            offset += 50

    def get_track_ids_from_playlist(self, playlist_id: str) -> KeysView:
        track_ids: Dict[str, None] = {}
        offset = 0
        while True:
            tracks = self.playlist_tracks(playlist_id, offset=offset)
            for track in tracks["items"]:
                track_ids[track["track"]["id"]] = None
            if tracks["next"] is not None:
                offset += 100
            else:
                break

        return track_ids.keys()

    @property
    def start_of_week(self) -> str:
        now = datetime.datetime.now()
        monday = now - datetime.timedelta(days=now.weekday())
        return monday.strftime("%B %d '%y")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PLAYLIST_NAME]",
        description="Set name of playlist to add to or use default",
    )
    parser.add_argument("-pn", "--playlist_name", default=None)
    args = parser.parse_args()
    spotify = Spotify(args.playlist_name)
    spotify.create_discover_weekly_playlist()
    print("success!")
