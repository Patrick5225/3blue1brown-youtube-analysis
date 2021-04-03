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

### MySQL Database Design
<img src="/images/youtube_diagram.PNG" width="700" height="350">

## MySQL Queries
### Q1: What are the top 5 most liked videos?
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
| title | publishDate | likeCount | 
| --- | --- | --- | 
| The hardest problem on the hardest test | 2017-12-08 15:04:57 | 240937 | 
| But what is a Neural Network? \| Deep learning, chapter 1 | 2017-10-05 15:11:25 | 221164 | 
| But how does bitcoin actually work? | 2017-07-07 16:51:37 | 177288 
| But what is the Fourier Transform?  A visual introduction. | 2018-01-26 18:47:48 | 165947 | 
| Exponential growth and epidemics | 2020-03-08 16:58:19 | 164994 | 

<img src="/images/top_5_liked_videos.png" width="700" height="350">

### Q2: Which videos have the highest dislike percentage?
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
| title | Dislike Ratio | likeCount | dislikeCount | 
| --- | --- | --- | --- | 
| e to the pi i, a nontraditional take (old version) | 7.05% | 33773 | 2561 | 
| What does it feel like to invent math? | 4.52% | 55179 | 2615 | 
| Triangle of Power | 2.35% | 22432 | 540 | 
| Thinking outside the 10-dimensional box | 2.30% | 53075 | 1251 | 
| Q&A #2 + Net Neutrality Nuance | 2.24% | 4620 | 106 | 

<img src="/images/dislike_ratio.png" width="900" height="400">

### Q3: Which users have commented the most often across all the YouTube videos from 3Blue1Brown?
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
| authorId | authorName | Number of Comments | 
| --- | --- | --- | 
| UCGhQcael1605jqEQJQgIUJg | David Wilkie | 102 | 
| UC9g0x_azdSh_3CoEUQCfidA | John Chessant | 77 |
| UC_0BFJBpSy9BJkjuFeX7I3Q | somi park | 77 | 
| UCYO_jab_esuFRV4b17AJtAw | 3Blue1Brown | 60 | 
| UC6Y0aX87IKzqWAwATTUYIkw | Henry G. | 58 | 
| UCNffOmAuakIYHEU8fEMfV6g | Ryan R | 58 | 
| UC86zgEvj-YmvKsPLASyK3rQ | Technoultimategaming | 54 | 
| UC7ESLeR1s4C95FNZBDADDIA | Zairaner | 52 | 
| UCH8wirhQN2P-lA3AwAicIcA | ganondorfchampin | 48 | 
| UCAoMJHYqv3_1V_WRE5TvH8Q | Holobrine | 47 | 

<img src="/images/top_commentors.png" width="700" height="350">

### Q4: For the user who has the most amount of comments, what were the top 5 videos that they commented on?
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
| title | Commentor Name | Number of Comments | 
| --- | --- | --- | 
| Euler's formula with introductory group theory | David Wilkie | 6 | 
| Visualizing the Riemann zeta function and analytic continuation | David Wilkie | 6 | 
| But what is a Fourier series? From heat flow to circle drawings \| DE4 | David Wilkie | 4 | 
| Some light quantum mechanics (with minutephysics) | David Wilkie | 3 | 
| Why 5/3 is a fundamental constant for turbulence | David Wilkie | 3 | 

<img src="/images/top_commentor_videos.png" width="800" height="350">

### Q5: Which comment has the most amount of likes, and on which video was it commented on?
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

| title | video_comment | authorName | likeCount | totalReplyCount | 
| --- | --- | --- | --- | --- | 
| The unexpectedly hard windmill question (2011 IMO, Q2) | "I know what you're thinking, those do happen to be all prime numbers"</br></br>nah I wasn't thinking that | gdhr | 26723 | 112 | 
