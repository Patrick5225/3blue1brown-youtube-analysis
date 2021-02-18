'''
author: Patrick Chao
about: This file extracts comments (not including replies) for each YouTube
video using its video id.
'''

import requests
import json
import pandas as pd
import time
from tqdm import tqdm

API_KEY = 'enter_key_here'
nextToken = '' # used for navigating through pages

# copied and pasted from video_ids.py
videoIds = ['lG4VkPoG3ko', 'b3NxrZOu_CE', 'X8jsijhllIA', 'mH0oCDa74tE', 'wTJI_WuZSwE',
            'QvuQH4_05LI', 'pq9LcwC7CoY', 'D__UaR5MQao', 'elQVZLLiod4', '4PDoT7jtxmw',
            'cEvgcoyZvB4', 'IAEASE5GjdI', 'ZxYOEwM6Wbk', '5PcpBw5Hbwo', 'yBw67Fb31Cs', 
            'MHXO86wKeDY', 'ppWPuXsnf1Q', 'ZA4JkHKZM50', 'gxAaO2rsdIs', '8idr1WZ1A7Q', 
            'Kas0tIxDvrg', 'U_85TaXbeIo', 'HZGCoVF3YvM', 'Agbh95KyWxY', 'EK32jo7i5LQ', 
            'M64HUIJFTZM', 'v0YEaeIClKY', '-qgreAUpPwM', 'r6sGWTCMz2k', 'ToIXSwZ1pJU', 
            'ly4S0oi3Yz8', 'p_di4Zn4wz4', 'jBsC34PxzoM', 'brU5yLm9DZM', 'jsYwFizhncE', 
            'HEfHFsfGXjs', 'GNcFjFmqEc8', 'yuVqxCSsE7c', '_UoTTq651dE', 'zjMuIxRvygQ', 
            'd4EgbgTm0Bg', 'Qe6o9j4IjTo', 'pQa_tWZmlGs', 'VcgJro0sTiM', 'rB83DpBJQsE', 
            'CfW845LNObM', '8GPy_UMV-08', 'b7FxPsqfkOY', 'bcPTiiiYDs8', 'd-o3eB9sfls', 
            'MBnnXbOM5S4', 'spUNpyF58BY', 'VvCytJvd4H0', 'liL66CApESk', 'OkmNXy7er84', 
            'tIeHLnjs5U8', 'Ilg3gGewQ5U', 'IHZwWFHWa-w', 'aircAruvnKk', 'MzRCDLre1b4', 
            'zwAD6dRSVyI', '3s7h2MHQtxc', 'S9JGmA5_unY', 'bBC-nXj3Ng4', 'QJYmyhnaaek', 
            'NaL_Cb42WyY', '3d6DsjIBzJ4', 'BLkz5LGWihw', 'FnJqaIESC2s', 'rfG8ce4nNh0', 
            'kfF40MiS7zA', 'qb40J4N1fa4', 'm2MIpDrF7Es', 'YG15m2VwSjA', 'S0_qX4VJhMQ', 
            '9vKqVkMQHKk', 'WUvTyaaNkzM', 'mvmuCPvRoWQ', 'gB9n2gHsHN4', 'IxNb1WG_Ido', 
            'sD0NjbwqlYw', 'bdMfjfT0lKk', 'R7p-nPg8t_g', '2SUvWfNJSsM', 'AmgkSdhK4K8', 
            'TgKwz5Ikpc8', 'PFDu9oVAE-g', 'P2LTAUO1TdA', 'BaM7OCEm3G0', 'eu6i7WJeinw', 
            'LyGKycYT2v0', 'v8VSDg_WQlA', 'uQhTuRlWMxw', 'Ip3X9LOh2dk', 'rHLEWRxRGiM', 
            'XkY2DOUCWMU', 'kYB8IZa5AuE', 'k7RM-ot2NWY', 'fNk_zzaMoSs', 'kjBOesZCoqc', 
            'sULa9Lc4pck', 'Iq1a_KJTWJ8', 'Cld0p3a43fU', 'RU0wScIj36o', 'cyW5z-M2yzw', 
            '1SMmc9gQmHQ', 'XFDM1ip5HdU', '-9OUyo8NFZg', 'K8P8uFahAgc', '84hEmGHw3J8', 
            'zLzLxVeqdQg']

comments = []

for id in tqdm(videoIds):
    while(True):
            response = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?&key="+API_KEY+"&part=snippet"+"&videoId="+id+"&maxResults=100"+"&pageToken="+nextToken)

            data = response.json()

            # if an error occurs, print data up to error
            if 'error' in data:
                print(data)
                break

            # obtain data for each YouTube comment
            for item in data['items']:
                try:
                    snippet = {
                        'videoId':item['snippet']['videoId'],
                        'commentId':item['snippet']['topLevelComment']['id'],
                        'comment':item['snippet']['topLevelComment']['snippet']['textOriginal'],
                        'authorName':item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'authorId':item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'],
                        'likeCount':item['snippet']['topLevelComment']['snippet']['likeCount'],
                        'date':item['snippet']['topLevelComment']['snippet']['updatedAt'],
                        'totalReplyCount':item['snippet']['totalReplyCount']
                    }
                except:
                    # in case there are missing fields
                    pass

                comments.append(snippet)

            # go to nextpage of comments until there is no nextpage
            if 'nextPageToken' in data:
                nextToken = data['nextPageToken']
            else:
                time.sleep(0.3)
                break

# use StringIO for reading json file
from io import StringIO

# convert into JSON string
review_dump = json.dumps(comments,indent=4)
df = pd.read_json(StringIO(review_dump))

# convert into a csv file
fileName = 'youtube_comments.csv'
df.to_csv(fileName,index=False,encoding='utf-8')