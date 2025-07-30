# youtube_py2 パッケージ初期化ファイル
__version__ = "1.0.26"

import os
import sys


def _show_discontinued_message():
    """廃止メッセージを表示"""
    print("=" * 60)
    print("⚠️ このライブラリの開発・保守は終了しました")
    print("⚠️ This library is no longer maintained")
    print("=" * 60)
    print("本ライブラリは機能を提供していません。")
    print("This library does not provide any functionality.")
    print("=" * 60)


_show_discontinued_message()


# すべての機能を無効化
class _DisabledClass:
    """無効化されたクラス"""
    def __init__(self, *args, **kwargs):
        raise RuntimeError("このライブラリは廃止されました。This library is discontinued.")

    def __getattr__(self, name):
        raise RuntimeError("このライブラリは廃止されました。This library is discontinued.")


# すべてのクラスを無効化されたクラスに置き換え
YouTubeVideo = _DisabledClass
YouTubeChannel = _DisabledClass
YouTubeComment = _DisabledClass
YouTubePlaylist = _DisabledClass
YouTubeCaptions = _DisabledClass
YouTubeAuth = _DisabledClass
YouTubeAnalytics = _DisabledClass
YouTubeExport = _DisabledClass
YouTubeAsync = _DisabledClass
YouTubeCLI = _DisabledClass
YouTubeLogger = _DisabledClass
YouTubeLive = _DisabledClass
YouTubeMembership = _DisabledClass
YouTubePagination = _DisabledClass
YouTubePubSub = _DisabledClass
YouTubeLocalization = _DisabledClass


def require_device_cert(*args, **kwargs):
    """無効化された関数"""
    raise RuntimeError("このライブラリは廃止されました。This library is discontinued.")

__all__ = [
    "YouTubeVideo", "YouTubeChannel", "YouTubeComment", "YouTubePlaylist", "YouTubeCaptions",
    "YouTubeAuth", "YouTubeAnalytics", "YouTubeExport", "YouTubeAsync", "YouTubeCLI", "YouTubeLogger",
    "YouTubeLive", "YouTubeMembership", "YouTubePagination", "YouTubePubSub", "YouTubeLocalization",
    "require_device_cert"
]
