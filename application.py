from parser import parse_json_tweet
from update_database import insert_tweet
import tweepy
import psycopg2
import json


def connect_to_twitter_oauth():
    file = open('credentials', 'r')
    creds_dict = {}
    for line in file:
        credential = line.split("=")
        value = credential[1]
        creds_dict[credential[0]] = value[0:len(value)-1]
    auth = tweepy.OAuthHandler(consumer_key=creds_dict['CONSUMER_KEY'], consumer_secret=creds_dict['CONSUMER_SECRET'])
    auth.set_access_token(creds_dict['ACCESS_TOKEN'], creds_dict['ACCESS_SECRET'])
    api = tweepy.API(auth)
    return api


def connect_to_database():
    file = open('dbconnectioncredentials', 'r')
    creds_dict = {}
    for line in file:
        credential = line.split("=")
        value = credential[1]
        creds_dict[credential[0]] = value[0:len(value)-1]
    connection = psycopg2.connect(
        host=creds_dict['SERVER'],
        dbname=creds_dict['DATABASE_NAME'],
        user=creds_dict['USER_NAME'],
        password=creds_dict['PASSWORD'],
        port=creds_dict['PORT']
    )
    return connection


def get_tweets(connection, api):
    hashtags = ["#brexit", "#brexitdeal", "#stopbrexit", "#brexitshambles", "#hardbrexit", "#GetBrexitDone"]

    for hashtag in hashtags:
        for entity in tweepy.Cursor(api.search, q=hashtag, rpp=10).items(100):
           tweet = parse_json_tweet(entity._json)
           # insert_tweet(connection, tweet)


def add_existing_tweets(connection, filename):
    """
    Function for adding to database tweets written into a file using json objects.
    Tweets are read then we create Tweet objects and write them into a file
    :param filename: Name of the file with written tweets
    :return:
    """
    file_content = open(filename).read()
    for tweet_json in file_content.splitlines():
        tweet = parse_json_tweet(json.loads(tweet_json))
        # insert_tweet(connection, tweet)


def main():
    conn = connect_to_database()
    api = connect_to_twitter_oauth()
    add_existing_tweets(conn, "tweets")
    get_tweets(conn, api)


if __name__ == '__main__':
    main()
