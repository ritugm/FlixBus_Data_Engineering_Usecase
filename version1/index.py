import logging
from util import (
    get_tweets_from_sample_data,
    getHashTags,
    search_flixbus_tweets_last_week,
    store_tweets,
    analyze_user_tweets,
    extract_tweet_data,
    get_most_activeday_and_three_hashtags,
    get_max_tweet_per_user,
    get_date_format,
    get_last_week_start_end_date
)

log_file_path = 'logs.txt'
logging.basicConfig(level=logging.DEBUG, filename=log_file_path, filemode='w')


# Extracting the twitter data from the file
twitter_data = get_tweets_from_sample_data('tweets.json')
if not twitter_data:
    logging.error("No data to process")
    exit(0)

# To add the custom date, please change custom_date to
# True and modify the values
custom_date = False
start_date = "2022-05-26"
end_date = "2022-06-02"

if not custom_date:
    # Extracting the date range from last available week and 
    # overide the start and end date
    start_date, end_date = get_last_week_start_end_date(twitter_data)
else:
    format = "%Y-%m-%d"
    # Check the custom start date
    start_date = get_date_format(start_date, format)
    # Check the custom end date
    end_date = get_date_format(end_date, format)

    if not start_date and end_date:
        # Defaulting it back to last 7 days
        # Extracting the date range for last available week
        logging.error("Custom date range is invalid, proceeding "
                      "with last week date range"
                      )
        start_date, end_date = get_last_week_start_end_date(twitter_data)

# Get the hashtags to filter
hashtags = getHashTags()

# Search for tweets with #FlixBus, during the last available week
flixbus_tweets_last_available_week = search_flixbus_tweets_last_week(
    twitter_data, start_date, end_date, hashtags
)

logging.info(
        '============================================================\n'
        'Tweets count with #Flixbus during the last available week is '
        f'{len(flixbus_tweets_last_available_week)}\n storing the result in '
        'flixbus_tweets_lastweek.json\n'
        '============================================================='
        )

store_tweets(
    'flixbus_tweets_lastweek.json',
    flixbus_tweets_last_available_week
)


# From the search results, extract information such as date time,
# all hashtags, is it a retweet?
extracted_tweets = extract_tweet_data(flixbus_tweets_last_available_week)
logging.info(
        'Length of the tweets with date time, all hashtags, retweet status is '
        f'{len(extracted_tweets)}\n storing the extracted data in '
        'extracted_tweet_data.json\n'
        '============================================================='
        )
store_tweets(
    'extracted_tweet_data.json',
    extracted_tweets
)


# Calculate per user statistics such as most recent number of followers, 
# most recent location, average tweet length, top five hashtags used
per_user_statistics = analyze_user_tweets(
    flixbus_tweets_last_available_week
)
logging.info(
        'Count of the Unique users present in the filtered data is '
        f'{len(per_user_statistics)}\n storing the results in '
        'per_user_statistics.json\n'
        '============================================================='
        )
store_tweets(
    'per_user_statistics.json',
    per_user_statistics
)


# Calculate most active day during the last week,
# Total number of tweets with at least 3 hashtags
active_day, three_hashtags_tweet = get_most_activeday_and_three_hashtags(extracted_tweets)

print(
    '=============================================================\n'
    f' Most active day during the given duration {start_date} - {end_date} is {active_day}\n',
    f'Total number of tweets with at least 3 hashtags : {three_hashtags_tweet}\n'
    '=============================================================\n'
)


# Calculate maximum number of tweets per user
max_tweet = get_max_tweet_per_user(per_user_statistics)

print(
    f' Maximum number of tweets per user : {max_tweet}\n',
    '============================================================='
)
