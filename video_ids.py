import json
import pandas as pd

# opening json file for youtube channel
file = "3blue1brown.json"
data = None
with open(file) as f:
    data = json.load(f)

# extract channel id and statistics
channel_id, stats = data.popitem()

# obtain video ids and print as a list 
video_data = stats["video_data"]
video_ids = list(video_data.keys())
print(video_ids)