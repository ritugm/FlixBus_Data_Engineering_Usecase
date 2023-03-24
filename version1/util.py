import json
import logging
from datetime import datetime, timedelta
from collections import Counter


def search_hashtag(
        user_hashtag_list,
        filtered_hashtag_list,
        ):
    set1 = set(user_hashtag_list)
    set2 = set(filtered_hashtag_list)
    return bool(set1 & set2)


def convert_createdtime_to_date(time: str, date=True):
    if date:
        return datetime.strptime(time, '%a %b %d %H:%M:%S %z %Y').date()
    else:
        return datetime.strptime(time, '%a %b %d %H:%M:%S %z %Y')


def get_date_format(string, format):
    try:
        datetime.strptime(string, format)
        return datetime.strptime(string, format).date()
    except ValueError:
        return False


def get_last_week_start_end_date(twitter_data):
    last_week_end_date = get_last_week(twitter_data)
    end_date = last_week_end_date
    start_date = end_date - timedelta(days=7)
    return (start_date, end_date)


def merge_counter(hashtag_counter_dict, new_hashtags):
    for hashtag in new_hashtags:
        if hashtag in hashtag_counter_dict:
            hashtag_counter_dict[hashtag] += 1
        else:
            hashtag_counter_dict[hashtag] = 1
    return hashtag_counter_dict


def store_tweets(name, result):
    try:
        with open('Results_Data/'+name, 'w') as f:
            json.dump(result, f)
            return True
    except Exception as e:
        logging.error(e)
        return False


def extract_hash_tags(
        tweet_hashtags_list_dict, consider_all_combination=False, count=False
        ):
    user_hashtag_list = []
    for hashtag in tweet_hashtags_list_dict:
        if 'text' in hashtag:
            if consider_all_combination:
                user_hashtag_list.append(hashtag['text'].lower())
            else:
                user_hashtag_list.append(hashtag['text'])
    if count:
        return user_hashtag_list[:count]
    return user_hashtag_list


def get_tweets_from_sample_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            input_list = json.loads(f.read())
            return input_list
    except FileNotFoundError:
        logging.error("tweets.json file is missing")
        return False


def get_last_week(twitter_data):
    latest_time = None
    for tweet in twitter_data:
        try:
            date_obj = datetime.strptime(tweet['created_at'],
                                         '%a %b %d %H:%M:%S %z %Y')
            if latest_time is None or date_obj > latest_time:
                latest_time = date_obj
        except ValueError:
            logging.warning("Ignoring invalid date string")
    if latest_time is None:
        logging.error("No valid date strings found")
        return None
    else:
        latest_date = latest_time.date()
        return latest_date


def getHashTags():
    return ['flixbus']


def search_flixbus_tweets_last_week(
        input_list,
        start_date,
        end_date,
        hashtags
        ):
    logging.info(
        f"Fetching the tweets for the duration\nStart date  : {start_date}\n"
        f"End date  : {end_date}"
        )
    filtered_last_week_tweets = []
    for tweet in input_list:
        tweet_date = convert_createdtime_to_date(tweet['created_at'])
        if tweet_date >= start_date and tweet_date <= end_date:
            # Generate user hashtag list

            # Handle the hashtags missing case
            user_hashtag_list = []
            if 'hashtags' in tweet['entities']:
                # Toggle it based on the requirment
                consider_all_combination = True
                user_hashtag_list = extract_hash_tags(
                    tweet['entities']['hashtags'], consider_all_combination
                )

            if search_hashtag(
                user_hashtag_list,
                hashtags,
            ):
                # Results to be stored in the Flixbus_tweets_lastweek.json file
                filtered_last_week_tweets.append(tweet)

    return filtered_last_week_tweets


def extract_tweet_data(input_list):
    processed_tweets = {}
    for tweet in input_list:
        if 'id' not in tweet:
            logging.error('Invalid tweet_id')
            continue
        tweet_id = tweet['id']
        processed_tweets[tweet_id] = {
            'date_time': tweet['created_at'],
            'hashtags': extract_hash_tags(
                    tweet['entities']['hashtags'], True
                ),
            'isRetweet': True if 'retweeted_status' in tweet else False
        }

    return processed_tweets


def analyze_user_tweets(input_list):
    processed_data = {}
    for tweet in input_list:
        # Check if user data is present in the tweet
        tweet_id = 'Not Present'
        if tweet['id']:
            tweet_id = tweet['id']

        if 'user' in tweet and 'id' in tweet['user']:
            user_id = tweet['user']['id']
            hashtags = extract_hash_tags(
                tweet['entities']['hashtags'],
                True,
                5
            )
            if user_id not in processed_data:
                processed_data[user_id] = {
                    # Created_at
                    'created_at': tweet['created_at']
                    if 'created_at' in tweet else None,
                    # Most recent number of followers
                    'most_recent_followers': tweet['user']['followers_count']
                    if 'followers_count' in tweet['user'] else None,
                    # Most recent location
                    'most_recent_location': tweet['user']['location']
                    if 'location' in tweet['user'] else None,
                    # Average tweet length
                    'average_tweet_length': len(tweet['text'])
                    if 'text' in tweet else None,
                    # Top five hashtags used
                    'top_five_hashtags_used': hashtags,
                    # hashtag counter
                    'hashtagcounter': Counter(hashtags),
                    # count of tweets
                    'no_of_tweets': 1

                }

            else:
                if convert_createdtime_to_date(
                    processed_data[user_id]['created_at'], False
                ) < convert_createdtime_to_date(
                    tweet['created_at'], False
                ):
                    processed_data[user_id] = {
                        # Created_at
                        'created_at': tweet['created_at']
                        if 'created_at' in tweet else None,
                        # Most recent number of followers
                        'most_recent_followers':
                        tweet['user']['followers_count']
                        if 'followers_count' in tweet['user'] else None,
                        # Most recent location
                        'most_recent_location': tweet['user']['location']
                        if 'location' in tweet['user'] else None,
                    }
                # Average tweet length calculations
                curr_avg = (
                    processed_data[user_id]['average_tweet_length'] +
                    len(tweet['text'])) // 2
                processed_data[
                    user_id
                    ]['average_tweet_length'] = curr_avg               
                # top 5 hashtags calculations
                merged_counter = merge_counter(
                    processed_data[user_id]['hashtagcounter'],
                    hashtags)
                processed_data[user_id][
                    'hashtagcounter'
                    ] = merged_counter

                top_5_hashtags = [k for k, v in sorted(merged_counter.items(),
                                                     key=lambda x: x[1],
                                                     reverse=True)][:5]
                processed_data[user_id][
                    'top_five_hashtags_used'
                    ] = top_5_hashtags

                # No of tweets
                processed_data[user_id][
                    'no_of_tweets'
                    ] += 1
        else:
            logging.error(f'Invalid user for tweet_id : {tweet_id}')

    return processed_data


def get_most_activeday_and_three_hashtags(input_list):
    active_day_map = {}
    tweet_count = 0
    if not input_list:
        return (0, 0)
    for tweet_id in input_list:
        #  Most active day during the last week
        date_time = convert_createdtime_to_date(input_list[tweet_id]['date_time'])
        if date_time not in active_day_map:
            active_day_map[date_time] = 1
        else:
            active_day_map[date_time] += 1

        # Total number of tweets with atleast three hashtags
        if len(input_list[tweet_id]['hashtags']) >= 3:
            tweet_count += 1
    date = [k for k, v in sorted(
        active_day_map.items(),
        key=lambda x: x[1],
        reverse=True)][:1][0]
    return (date, tweet_count)


def get_max_tweet_per_user(input_list):
    if not input_list:
        return 0
    maxTweet = None
    for user_id in input_list:
        no_of_tweets = input_list[user_id]['no_of_tweets']
        if not maxTweet:
            maxTweet = no_of_tweets
        if no_of_tweets > maxTweet:
            maxTweet = no_of_tweets
    return maxTweet
