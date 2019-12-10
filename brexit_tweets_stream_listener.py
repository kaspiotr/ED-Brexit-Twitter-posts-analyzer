import tweepy
import json
import jsonlines
import os
from utils import insert_month_no


# override tweepy.StreamListener to add logic to on_data

class BrexitTweetsStreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        tweet_dict = json.loads(raw_data)
        file_date_list = tweet_dict['created_at'].split()
        with jsonlines.open(
                os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + '/backup/tweets' + "_" + file_date_list[-1] + "_" + insert_month_no(file_date_list[1]) + "_" + file_date_list[2], mode='a') as writer:
            writer.write(tweet_dict)
        return True

    def on_error(self, status_code):
        print("On error=========")
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
        # returning non-False reconnects the stream, with backoff.
