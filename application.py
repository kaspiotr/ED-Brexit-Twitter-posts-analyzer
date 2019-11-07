import tweepy
import psycopg2


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


def main():
    api = connect_to_twitter_oauth()

    for tweet in tweepy.Cursor(api.search, q='#brexit', rpp=100).items(100):
        print(tweet.text)
        print("Retweets no.: %d" % tweet.retweet_count)

    conn = connect_to_database()
    print("connected")
    cursor = conn.cursor()
    print(cursor.execute('SELECT * FROM postgres.public.users'))


if __name__ == '__main__':
    main()
