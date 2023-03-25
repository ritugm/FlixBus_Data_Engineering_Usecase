# Data Engineering Use Case For FlixBus

This project aims to search for tweets with the hashtag #FlixBus during the last available week and extract some specific data. The data includes the date and time of the tweet, the hashtag(s) used in the tweet, and whether it is a retweet or not. After parsing the data, we will calculate various metrics per user, such as the most recent number of followers, most recent location, average tweet length, top five hashtags used. Other metrics such as most active day during the last week, the total number of tweets with at least three hashtags, and the maximum number of tweets per user are also calculated.

## Sample Data

A sample dataset in JSON format included in tweets.json is used for testing and development purposes.

## Process Overview

1. Load the sample dataset (tweets.json)
2. Filter the tweets to include only those with the hashtag #flixbus and within the last available week's date range and store the results data in a *flixbus_tweets_lastweek.json* file.
3. Extract the following data from the filtered tweets and store it in *extracted_tweet_data.json* file.
   - Date time of the tweet
   - Hashtag(s) used in the tweet
   - Is it a retweet?
4. After data parsing, calculate various metrics per user and store the results in *per_user_statistics.json* file.
   - Per user:
      1. Most recent number of followers
      2. Most recent location
      3. Average tweet length
      4. Top five hashtags used
5. The program will output the below calculated metrics to the console.
   - Most active day during the last week
   - Total number of tweets with at least three hashtags
   - Maximum number of tweets per user

## Technologies Used

The project is implemented using Python programming language (version 3.0 or higher).

## Libraries Used

The following libraries were used in this project:
- logging: for handling log messages from Python
- datetime: for handling dates and times
- json: for loading the sample dataset
- collections: for handling collections of related data


## Usage

1. Clone this repository to your local machine.
2. Run the program by executing the index.py file from the **version1** directory (`cd version1`, `python index.py`)
3. The program will output the results in these 3 files under the **version1/Results_Data** directory - *flixbus_tweets_lastweek.json*, *extracted_tweet_data.json*, *per_user_statistics.json*.
4. The program will also output all the logs to the *logs.txt* file under the **version1** directory.
5. The program will also output a few calculated metrics such as *most active day during the last week*, *total number of tweets with at least three hashtags*, and *maximum number of tweets per user* directly to the **console**.