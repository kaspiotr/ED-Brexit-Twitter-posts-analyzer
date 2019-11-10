def insert_tweet(connection, tweet):
    # think if it's not better to give a list of tweets as a parameter
    cursor = connection.cursor()
    query = "INSERT INTO tweets(id, userId, fullText, createdAt, inReplyToTweetId, inReplyToUserId,) " \
            "VALUES(%s, %s, %s, %s, %s, %s)"
    data = (tweet.id, tweet.user_id, tweet.full_text, tweet.created_at, tweet.in_reply_to_tweet_id, tweet.in_reply_to_user_id)
    cursor.execute(query, data)
    connection.commit()
