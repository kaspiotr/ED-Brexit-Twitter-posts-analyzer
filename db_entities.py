class User:
    id = None
    name = None
    user_name = None
    location = None
    language = None
    tweets_number = None

    def __init__(self, id, name, user_name, location, language, tweets_number):
        self.id = id
        self.name = name
        self.user_name = user_name
        self.loacation = location
        self.language = language
        self.tweets_number = tweets_number


class Tweet:
    id = None
    user_id = None
    full_text = None
    created_at = None
    retweets_number = None
    likes_number = None
    comments_number = None
    in_reply_to_tweet_id = None
    in_reply_to_user_id = None
    sentiment = None

    def __init__(self, id, user_id, content, created_at, retweets_number, likes_number, comments_number, in_reply_to_tweet_id, in_reply_to_user_id, sentiment):
        self.id = id
        self.user_id = user_id
        self.full_text = content
        self.created_at = created_at
        self.retweets_number = retweets_number
        self.likes_number = likes_number
        self.comments_number = comments_number
        self.in_reply_to_tweet_id = in_reply_to_tweet_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.sentiment = sentiment


class MarkedUser:
    tweet_id = None
    user_id = None

    def __init__(self, tweet_id, user_id):
        self.tweet_id = tweet_id
        self.user_id = user_id


class Hashtag:
    id = None
    name = None

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Retweet:
    tweet_id = None
    user_id = None

    def __init__(self, tweet_id, user_id):
        self.tweet_id = tweet_id
        self.user_id = user_id
