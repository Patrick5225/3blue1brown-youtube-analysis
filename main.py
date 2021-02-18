'''
author: Patrick Chao
about: This file is the main file used to obtain statistics
for a specific YouTube channel along with data for each video.
Use along with youtube_statistics.py
'''

from youtube_statistics import YTstats

# api key hidden. Visit YouTube's official Data API website to obtain key
API_KEY = "enter_key_here"

# ID for 3blue1brown
channel_id = "UCYO_jab_esuFRV4b17AJtAw"

yt = YTstats(API_KEY, channel_id)
yt.get_channel_statistics()
yt.get_channel_video_data()
yt.dump()