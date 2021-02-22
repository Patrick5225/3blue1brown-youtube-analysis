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

## MySQL Database Design
<img src="/images/youtube_diagram.PNG" width="700" height="350">

## MySQL Queries
### What are the top 5 most liked videos?

<img src="/images/query_top_5_liked_videos.PNG" width="600" height="400">

### Which videos have the highest dislike percentage?
<img src="/images/query_dislike_ratio.PNG" width="900" height="500">

### Which users have commented the most often across all the YouTube videos from 3Blue1Brown?
<img src="/images/query_top_commentors.PNG" width="700" height="500">

### For the user who has the most amount of comments, what were the top 5 videos that they commented on?
<img src="/images/query_top_commentor_videos.PNG" width="800" height="500">

## MySQL: Importing Data and Creating Tables

### Importing the Data
<img src="/images/sql_loading_data.PNG" width="900" height="500">

### Creating the Schema and Tables
<img src="/images/sql_table1.PNG" width="400" height="400">

<img src="/images/sql_table2.PNG" width="400" height="400">
