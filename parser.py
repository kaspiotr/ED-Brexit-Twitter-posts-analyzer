from db_entities import Tweet


def parse_json_tweet(json_tweet):
    tweet_id = json_tweet["id"]
    tweet_user_id = json_tweet["user"]["id"]
    tweet_full_text = json_tweet["text"]
    tweet_created_at = json_tweet["created_at"]
    tweet_retweets_number = json_tweet["retweet_count"]
    tweet_likes_number = json_tweet["favorite_count"]
    tweet_comments_number = None
    tweet_in_reply_to_tweet_id = json_tweet["in_reply_to_status_id"]
    tweet_in_repl_to_user_id = json_tweet["in_reply_to_user_id"]
    tweet = Tweet(tweet_id, tweet_user_id, tweet_full_text, tweet_created_at, tweet_retweets_number, tweet_likes_number, tweet_comments_number, tweet_in_reply_to_tweet_id, tweet_in_repl_to_user_id)





