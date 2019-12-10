import tweepy
from brexit_tweets_stream_listener import BrexitTweetsStreamListener


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
    brexit_tweets_stream_listener = BrexitTweetsStreamListener()
    brexit_tweets_stream = tweepy.Stream(auth=api.auth, listener=brexit_tweets_stream_listener)
    brexit_tweets_stream.filter(track=['#brexit', '#stopbrexit', '#brexitshamples', '#brexitdeal', '#hardbrexit', '#GetBrexitDone'])


if __name__ == '__main__':
    main()
