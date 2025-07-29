# __init__.py

from youtube_py3.base import YouTubeAPIClient
from youtube_py3.videos import Videos
from youtube_py3.channels import Channels
from youtube_py3.playlists import Playlists
from youtube_py3.search import Search
from youtube_py3.comments import Comments
from youtube_py3.config_util import ConfigUtil
from youtube_py3.oauth_util import OAuthUtil

class YouTube:
    def __init__(self, api_key: str):
        self.client = YouTubeAPIClient(api_key)
        self.videos = Videos(self.client)
        self.channels = Channels(self.client)
        self.playlists = Playlists(self.client)
        self.search = Search(self.client)
        self.comments = Comments(self.client)
        self.config_manager = ConfigUtil()
        self.oauth_manager = OAuthUtil()

__all__ = ["YouTube"]
