# Nuitkaでバイナリ化したモジュール用の__init__.py
import youtube_py3.base
import youtube_py3.videos
import youtube_py3.channels
import youtube_py3.playlists
import youtube_py3.search
import youtube_py3.comments
import youtube_py3.config_util
import youtube_py3.oauth_util

class YouTube:
    def __init__(self, api_key: str):
        self.client = youtube_py3.base.YouTubeAPIClient(api_key)
        self.videos = youtube_py3.videos.Videos(self.client)
        self.channels = youtube_py3.channels.Channels(self.client)
        self.playlists = youtube_py3.playlists.Playlists(self.client)
        self.search = youtube_py3.search.Search(self.client)
        self.comments = youtube_py3.comments.Comments(self.client)
        self.config_manager = youtube_py3.config_util.ConfigUtil()
        self.oauth_manager = youtube_py3.oauth_util.OAuthUtil()
