# youtube_py2 パッケージ初期化ファイル
__version__ = "1.0.15"

# --- 改ざん検知・アンチデバッグを__init__.pyで実行 ---
import os
import sys
from youtube_py2 import _bootstrap
try:
    _bootstrap._detect_debugger()
except Exception as e:
    print(f"[アンチデバッグ] {e}", file=sys.stderr)
    os._exit(1)
_bootstrap._internal_update()

# 主要APIクラスをトップレベルで再エクスポート
from .video import YouTubeVideo
from .channel import YouTubeChannel
from .comment import YouTubeComment
from .playlist import YouTubePlaylist
from .captions import YouTubeCaptions
from .auth import YouTubeAuth
from .analytics import YouTubeAnalytics
from .export import YouTubeExport
from .async_api import YouTubeAsync
from .cli import YouTubeCLI
from .logging import YouTubeLogger
from .live import YouTubeLive
from .membership import YouTubeMembership
from .pagination import YouTubePagination
from .pubsub import YouTubePubSub
from .localization import YouTubeLocalization
from .license import require_device_cert

__all__ = [
    "YouTubeVideo", "YouTubeChannel", "YouTubeComment", "YouTubePlaylist", "YouTubeCaptions",
    "YouTubeAuth", "YouTubeAnalytics", "YouTubeExport", "YouTubeAsync", "YouTubeCLI", "YouTubeLogger",
    "YouTubeLive", "YouTubeMembership", "YouTubePagination", "YouTubePubSub", "YouTubeLocalization",
    "require_device_cert"
]
