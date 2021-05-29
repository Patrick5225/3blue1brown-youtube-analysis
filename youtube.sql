/*
author: Patrick Chao
about: This sql file was created using MySQL Workbench. It creates a schema
with tables, and inserts data imported from csv files containing YouTube video stats and comments.
*/

# setting up schemas and tables
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
    
# run these to enable loading local data
SHOW GLOBAL VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile=1;
    
# importing data from csv files
LOAD DATA LOCAL INFILE 'D:\\patri\\Documents\\Github\\3blue1brown-youtube-analysis\\data\\youtube_stats.csv'
INTO TABLE video_stats
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'D:\\patri\\Documents\\Github\\3blue1brown-youtube-analysis\\data\\youtube_comments.csv'
INTO TABLE comments
CHARACTER SET latin1
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# selecting to check that insertion were successful
SELECT * FROM video_stats;

-- With our tables successfully created with data inserted, we can query our data with questions such as:

# What are the top 5 most liked videos?
SELECT
	title,
    publishDate, 
    likeCount
FROM video_stats
GROUP BY videoId
ORDER BY likeCount DESC
LIMIT 5;

# Which videos have the highest dislike ratio?
SELECT
	title, 
    CONCAT(ROUND(dislikeCount/(likeCount+dislikeCount) * 100, 2),'%') AS 'Dislike Ratio',
    likeCount, 
    dislikeCount
FROM video_stats
GROUP BY videoId
ORDER BY 2 DESC
LIMIT 5;

# Which users have commented most often across all the videos from 3blue1brown?
SELECT
	authorId, 
    authorName, 
    COUNT(authorName) AS 'Number of Comments'
FROM comments
GROUP BY authorId
ORDER BY COUNT(authorName) DESC
LIMIT 10;

# For the user who has commented the most, what were the top 5 videos that the user has commented on?
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

# Which comment has the most amount of likes?
SELECT
	s.title, c.video_comment, c.authorName, c.likeCount, c.totalReplyCount
FROM video_stats s
INNER JOIN comments c
	ON s.videoId = c.videoId
WHERE c.likeCount = (SELECT
						MAX(likeCount)
					FROM comments);