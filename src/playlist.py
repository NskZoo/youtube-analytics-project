import datetime
from googleapiclient.discovery import build
import isodate
import os
from dotenv import load_dotenv

load_dotenv()


class PlayList:
    """
    Инициализация объекта PlayList с заданным идентификатором плейлиста
    """

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_info = youtube.playlists().list(id=playlist_id, part='contentDetails, snippet').execute()
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails, snippet',
                                                            maxResults=50).execute()
        video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()
        self.video_response = video_response
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        """
        Вычисление общей продолжительности видео в плейлисте
        """
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
            print(duration)
        return total_duration

    def show_best_video(self):
        """
        Вывод наиболее популярного видео в плейлисте по количеству лайков
        """
        max_like_count = 0
        best_video_id = ''
        for video in self.video_response['items']:
            like_count = int(video['statistics'].get('likeCount', 0))
            if like_count > max_like_count:
                max_like_count = like_count
                best_video_id = video['id']
                print(f"https://youtu.be/{best_video_id}")
        return f"https://youtu.be/{best_video_id}"
