import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
load_dotenv()


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.youtube = self.get_service()
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube/channels/{self.__channel_id}"
        self.subscriber_count = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API-KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file_json):
        json_data = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'descrition': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'videoCount': self.video_count,
            'viewCount': self.view_count
        }
        with open(file_json, 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False, indent=4))

    @channel_id.setter
    def channel_id(self, value):
        self.__channel_id = value

    def __str__(self):
        return f"{self.title}, {self.url}"

    def __add__(self, other):
        """оператор сложения"""
        if isinstance(other, Channel):
            return int(self.subscriber_count) + int(other.subscriber_count)
        else:
            raise TypeError("Неподдерживаемый тип операнда для +: 'Channel' и {}".format(type(other)))

    def __sub__(self, other):
        """оператор вычитания"""
        if isinstance(other, Channel):
            return int(self.subscriber_count) - int(other.subscriber_count)
        else:
            raise TypeError("Неподдерживаемый тип операнда для -: 'Channel' и {}".format(type(other)))

    def __lt__(self, other):
        """оператор меньше (<)"""
        if isinstance(other, Channel):
            return int(self.subscriber_count) < int(other.subscriber_count)
        else:
            raise TypeError("Неподдерживаемый тип операнда для <: 'Channel' и {}".format(type(other)))

    def __le__(self, other):
        """оператор меньше или равно (<=)"""
        if isinstance(other, Channel):
            return int(self.subscriber_count) <= int(other.subscriber_count)
        else:
            raise TypeError("Неподдерживаемый тип операнда для <=: 'Channel' и {}".format(type(other)))

    def __eq__(self, other):
        """оператор равенства (==)"""
        if isinstance(other, Channel):
            return int(self.subscriber_count) == int(other.subscriber_count)
        else:
            raise TypeError("Неподдерживаемый тип операнда для ==: 'Канал' и {}".format(type(other)))

    def __ne__(self, other):
        """оператор неравенства (!=)"""
        if isinstance(other, Channel):
            return int(self.subscriber_count) != int(other.subscriber_count)
        else:
            raise TypeError("Неподдерживаемый тип операнда для !=: 'Channel' и {}".format(type(other)))

    def __gt__(self, other):
        """оператор больше (>)"""
        if isinstance(other, Channel):
            return int(self.subscriber_count) > int(other.subscriber_count)
        else:
            raise TypeError("Неподдерживаемый тип операнда для >: 'Channel' и {}".format(type(other)))

    def __ge__(self, other):
        """оператор больше
        или равно (>=)"""
        if isinstance(other, Channel):
            return int(self.subscriber_count) >= int(other.subscriber_count)
        else:
            raise TypeError("Неподдерживаемый тип операнда для >=: 'Channel' и {}".format(type(other)))

