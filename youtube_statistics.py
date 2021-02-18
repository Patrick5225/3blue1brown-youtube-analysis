'''
author: python-engineer
url: https://github.com/python-engineer/youtube-analyzer
about: This file contains code which starts on python-engineer code and is 
then modified by me. The file mainly extracts youtube statistics of a channel and also
statistics for each video, all while using a YouTube API.
'''

import requests
import json
import time
from tqdm import tqdm

# import this class into main.py
class YTstats:
    def __init__(self, api_key, channel_id):
        '''
        The api_key and channel_id are from main.py
        '''
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None

    def get_channel_statistics(self):
        '''
        Get channel statistics such as total views and subcribers
        '''
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0]["statistics"]
        except:
            data = None

        self.channel_statistics = data
        return data

    def get_channel_video_data(self):
        '''
        Get video statistics such as likes/dislikes using video id
        '''

        # 1) get video ids
        channel_videos = self._get_channel_videos(limit=50)
        print(len(channel_videos))

        # 2) get video statistics
        parts = ["snippet", "statistics"]
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self._get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)
                time.sleep(0.3)

        self.video_data = channel_videos
        return channel_videos

    def _get_single_video_data(self, video_id, part):
        '''
        Get certain information for a video such as its statistics
        '''
        url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0][part]
        except:
            print("error")
            data = dict()

        return data

    def _get_channel_videos(self, limit=None):
        '''
        Obtain all video ids for youtube channel
        '''
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date"
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
        
        vid, npt = self._get_channel_videos_per_page(url)
        idx = 0
        while(npt is not None and idx < 10):
            nexturl = url + "&pageToken=" + npt
            next_vid, npt = self._get_channel_videos_per_page(nexturl)
            vid.update(next_vid)
            idx += 1

        return vid

    def _get_channel_videos_per_page(self, url):
        '''
        Navigation through pages of channel videos
        '''
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()
        if 'items' not in data:
            return channel_videos, None

        item_data = data['items']
        nextPageToken = data.get("nextPageToken", None)
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = dict()
            except KeyError:
                print("error")

        return channel_videos, nextPageToken

    def dump(self):
        '''
        Dump all data into a json file
        '''
        if self.video_data is None:
            print('No data for video data')
            return

        if self.channel_statistics is None:
            print('No data for channel statistics')
            return
        
        fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics, "video_data": self.video_data}}

        channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        channel_title = channel_title.replace(" ", "_").lower()
        file_name = channel_title + '.json'
        with open(file_name, 'w') as f:
            json.dump(fused_data, f, indent=4)

        print('file dumped')