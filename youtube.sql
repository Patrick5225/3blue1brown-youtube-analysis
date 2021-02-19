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
    
# importing data from csv files
LOAD DATA LOCAL INFILE 'D:\\patri\\Documents\\Github\\3blue1brown-youtube-analysis\\data\\youtube_stats.csv'
INTO TABLE video_stats
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'D:\\patri\\Documents\\Github\\3blue1brown-youtube-analysis\\data\\youtube_comments.csv'
INTO TABLE comments
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# selecting to check that insertion were successful
SELECT * FROM video_stats;