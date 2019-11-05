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


def main():
    api = connect_to_twitter_oauth()

    for tweet in tweepy.Cursor(api.search, q='#brexit', rpp=100).items(100):
        print(tweet.text)

    # connection with database
    server = "ec2-54-217-225-16.eu-west-1.compute.amazonaws.com"
    database = "d8raoh0vdr0n8q"
    username = "qcgqzcyhxmjkvi"
    password = "a0a102e858cee2eadf4a14cebf40e77659656cd7e9ef0d645759a68a3263053e"
    port = 5432

    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=server,
        port=port
    )

    print("connected")
    cursor = conn.cursor()
    print(cursor.execute('SELECT * FROM USERS'))


if __name__ == '__main__':
    main()
