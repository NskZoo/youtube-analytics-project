from googleapiclient.discovery import build
import os


class Video:
    def __init__(self, channel_id: str, youtube=build('youtube', 'v3', developerKey=os.getenv('API-KEY'))):

        self.channel_id = channel_id
        self.youtube = youtube
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])
        self.like_count = int(self.channel['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, channel_id: str, id_playlist: str):
        self.id_playlist = id_playlist
        super().__init__(channel_id)
