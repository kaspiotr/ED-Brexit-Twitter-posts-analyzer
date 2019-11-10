from itertools import takewhile

import tweepy
import psycopg2
import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


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


def get_tweets(api):
    # plt.rcParams.update({'font.size': 5})
    file = open('tweets', 'a')
    hashtags = ["#brexit", "#brexitdeal", "#stopbrexit", "#brexitshambles", "#hardbrexit", "#GetBrexitDone"]
    result = []

    for hashtag in hashtags:
        for tweet in tweepy.Cursor(api.search, q=hashtag, rpp=10).items(100):
            json_object = json.dumps(tweet._json)
            file.write(json_object + "\n")
            result.append((tweet.user.name, tweet.retweet_count, tweet.favorite_count))

    result.sort(key=lambda x: x[1])

    x = [x[0] for x in result[-10:]]
    y = [y[1] for y in result[-10:]]

    fig = plt.figure(figsize=(20, 15))
    ax = fig.add_subplot(111)
    ax.bar(np.arange(len(x)), y, log=1)
    ax.set_xticks(np.arange(len(x)))
    ax.set_xticklabels(x, rotation=45, zorder=100)
    ax.set_yticklabels(y)

    # fig.savefig(fname="most_retweet_users2.png")

    counts = Counter(x[0] for x in result)

    most_common = list(takewhile(lambda x: x[-1] > 1, counts.most_common()))
    x = [x[0] for x in most_common[:10]]
    y = [y[1] for y in most_common[:10]]

    ax.bar(np.arange(len(x)), y)
    ax.set_xticks(np.arange(len(x)))
    ax.set_xticklabels(x, rotation=45, zorder=100)
    ax.set_yticklabels(y)

    # fig.savefig(fname="most_active_users2.png")


def main():
    api = connect_to_twitter_oauth()

    for tweet in tweepy.Cursor(api.search, q='#brexit', rpp=100).items(100):
        print(tweet.text)
        print("Retweets no.: %d" % tweet.retweet_count)
    get_tweets(api)

    conn = connect_to_database()
    print("connected")
    cursor = conn.cursor()
    print(cursor.execute('SELECT * FROM postgres.public.users'))


if __name__ == '__main__':
    main()
