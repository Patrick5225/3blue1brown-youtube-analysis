<img src="/images/3blue1brown-banner.jpeg" width="900" height="300">

# 3Blue1Brown Youtube Channel Analysis
3Blue1Brown is a Youtube Channel that discusses higher-level mathematics with a visual approach, where the topics of mathematics discussed include Linear Algebra, Calculus, Fourier Transforms, etc. The goal of this project is to analyze 3Blue1Brown's YouTube videos and their comments to observe statistics such as views, likes/dislikes, and more.

## Project Overview
- Collected over 160,000 comments and video statistics of 112 YouTube videos using python and YouTube's API
- Cleaned data using python and Excel to fix data values and remove missing values
- Created a data model using MySQL Workbench and performed queries using SQL to answer questions about the data
- Visualized data with a dashboard using Tableau using visuals such as a line chart and text table

## Resources Used

**3Blue1Brown YouTube Channel**: https://www.youtube.com/c/3blue1brown</br>
**YouTube API Documentation**: https://developers.google.com/youtube/v3/docs</br>
**Collecting YouTube Statistics GitHub**: https://github.com/python-engineer/youtube-analyzer

## Tableau Dashboard
Tableau public: https://public.tableau.com/profile/patrick.chao#!/vizhome/3blue1brown/VideosDashboard

<img src="/images/tableau_dashboard.PNG" width="1000" height="500">

## MySQL: Creating Tables and Database Design
### Creating the Schema and Tables
```sql
CREATE SCHEMA youtube;

CREATE TABLE video_stats(
  videoId VARCHAR(30) NOT NULL PRIMARY KEY,
  title VARCHAR(200),
  publishDate DATETIME,
  video_description TEXT,
  viewCount INT,
  likeCount INT,
  dislikeCount INT,
  commentCount INT
);

CREATE TABLE comments(
  videoId VARCHAR(30) NOT NULL,
  commentId VARCHAR(50) NOT NULL PRIMARY KEY,
  video_comment TEXT,
  authorName VARCHAR(250),
  authorId VARCHAR(50),
  likeCount INT,
  commentDate DATETIME,
  totalReplyCount INT,
  FOREIGN KEY (videoId)
    REFERENCES video_stats(videoId)
);
```

## MySQL Database Design
<img src="/images/youtube_diagram.PNG" width="700" height="350">

## MySQL Queries
### What are the top 5 most liked videos?
```sql
SELECT
  title,
  publishDate,
  likeCount
FROM video_stats
GROUP BY videoId
ORDER BY likeCount DESC
LIMIT 5;
```
<img src="/images/top_5_liked_videos.png" width="700" height="350">

### Which videos have the highest dislike percentage?
```sql
SELECT
  title,
  CONCAT(ROUND(dislikeCount/(likeCount+dislikeCount) * 100, 2),'%') AS 'Dislike Ratio',
  likeCount,
  dislikeCount
FROM video_stats
GROUP BY videoId
ORDER BY 2 DESC
LIMIT 3;
```
<img src="/images/dislike_ratio.png" width="900" height="400">

### Which users have commented the most often across all the YouTube videos from 3Blue1Brown?
```sql
SELECT
  authorId,
  authorName,
  COUNT(authorName) AS 'Number of Comments'
FROM comments
GROUP BY authorId
ORDER BY COUNT(authorName) DESC
LIMIT 10;
```
<img src="/images/top_commentors.png" width="700" height="350">

### For the user who has the most amount of comments, what were the top 5 videos that they commented on?
```sql
SELECT
  s.title,
  c.authorName AS 'Commentor Name',
  COUNT(c.authorName) AS 'Number of Comments'
FROM video_stats s
INNER JOIN comments c
  ON s.videoId = c.videoId
WHERE authorId = (SELECT
                    authorId
                 FROM comments
                 GROUP BY authorId
                 ORDER BY COUNT(authorName) DESC
                 LIMIT 1)
GROUP BY s.title
ORDER BY COUNT(c.authorName) DESC
LIMIT 5;
```
<img src="/images/top_commentor_videos.png" width="800" height="350">

### Which comment has the most amount of likes, and on which video was it commented on?
```sql
SELECT
  s.title,
  c.video_comment,
  c.authorName,
  c.likeCount,
  c.totalReplyCount
FROM video_stats s
INNER JOIN comments c
  ON s.videoId = c.videoId
WHERE c.likeCount = (SELECT
                      MAX(likeCount)
                    FROM comments);
```
<img src="/images/query_most_liked_comment.PNG" width="800" height="350">


