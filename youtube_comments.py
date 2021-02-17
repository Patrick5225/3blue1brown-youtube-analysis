import requests
import json
import pandas as pd

API_KEY = 'enter_key_here'
nextToken = ''
videoId = 'enter_id_here'

comments = []

while(True):
        response = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?&key="+API_KEY+"&part=snippet"+"&videoId="+videoId +"&maxResults=100"+"&pageToken="+nextToken)

        data = response.json()

        # if an error occurs, print data up to error
        if 'error' in data:
            print(data)
            break

        for item in data['items']:
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

            comments.append(snippet)

        # go to nextpage of comments until there is no nextpage
        if 'nextPageToken' in data:
            nextToken = data['nextPageToken']
        else:
            break

# convert into JSON string
review_dump = json.dumps(comments,indent=4)
df = pd.read_json(review_dump)

# convert into a csv file
fileName = videoId + '.csv'
df.to_csv(fileName,index=False,encoding='utf-8')