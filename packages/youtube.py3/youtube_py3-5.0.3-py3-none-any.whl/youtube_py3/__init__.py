# __init__.py

from .base import YouTubeAPIClient
from .videos import Videos
from .channels import Channels
from .playlists import Playlists
from .search import Search
from .comments import Comments
from .config_util import ConfigUtil
from .oauth_util import OAuthUtil

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
