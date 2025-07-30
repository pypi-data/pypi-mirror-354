import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Optional, Dict, Any

class YTVideoClient:
    """
    YouTube動画・チャンネル情報取得用クラス
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("環境変数 YOUTUBE_API_KEY が設定されていません")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_channel_info(self, channel_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.youtube.channels().list(
                part='snippet,contentDetails',
                id=channel_id
            ).execute()
            if response['items']:
                return response['items'][0]
            return None
        except HttpError as e:
            print(f"チャンネル情報取得エラー: {e}")
            return None

    def get_latest_video(self, channel_id: str) -> Optional[Dict[str, Any]]:
        info = self.get_channel_info(channel_id)
        if not info:
            return None
        uploads_playlist_id = info['contentDetails']['relatedPlaylists']['uploads']
        try:
            playlist_response = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=1
            ).execute()
            if playlist_response['items']:
                return playlist_response['items'][0]['snippet']
            return None
        except HttpError as e:
            print(f"最新動画取得エラー: {e}")
            return None

    def get_video_statistics(self, video_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()
            if response['items']:
                return response['items'][0]['statistics']
            return None
        except HttpError as e:
            print(f"動画統計取得エラー: {e}")
            return None
