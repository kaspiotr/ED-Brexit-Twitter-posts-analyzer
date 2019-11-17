import psycopg2
import jsonlines
import os
import glob
import re


def connect_to_database():
    file = open('dbconnectioncredentials', 'r')
    creds_dict = {}
    for line in file:
        credential = line.split("=")
        value = credential[1]
        creds_dict[credential[0]] = value[0:len(value) - 1]
    connection = psycopg2.connect(
        host=creds_dict['SERVER'],
        dbname=creds_dict['DATABASE_NAME'],
        user=creds_dict['USER_NAME'],
        password=creds_dict['PASSWORD'],
        port=creds_dict['PORT']
    )
    return connection


def update_db(db_connection):
    path = os.path.dirname(os.path.abspath(__file__)) + '/backup/*'
    jsonl_files = glob.iglob(path)
    for jsonl_file in jsonl_files:
        with jsonlines.open(jsonl_file, mode='r') as reader:
            for tweet_dict in reader:
                insert_into_db(db_connection, tweet_dict)
    db_connection.close()


def insert_into_db(db_connection, tweet_dict):
    cursor = db_connection.cursor()
    full_text = _insert_text(tweet_dict)
    created_at = _insert_created_at(tweet_dict)

    user_dict = tweet_dict['user']
    if _is_retweet(tweet_dict['text']):
        postgres_insert_query = "INSERT INTO retweets (tweetid, userid) VALUES (%s, %s);"
        record_to_insert = (tweet_dict['retweeted_status']['id'], user_dict['id'])
        try:
            cursor.execute(postgres_insert_query, record_to_insert)
            db_connection.commit()
        except psycopg2.errors.ForeignKeyViolation:
            print('There were no tweet with id %s found in tweets table. Row was not inserted into retweets table' % tweet_dict['retweeted_status']['id'])
            db_connection.rollback()
        except psycopg2.errors.UniqueViolation:
            print('User with id %s has retweeted the same tweet (with id %s) once again' % (user_dict['id'], tweet_dict['retweeted_status']['id']))
    else:
        postgres_insert_query = "INSERT INTO tweets (id, userid, fulltext, createdat, inreplytotweetid, inreplytouserid) VALUES (%s, %s, %s, %s, %s, %s);"
        record_to_insert = (tweet_dict['id'], tweet_dict['user']['id'], full_text, created_at, tweet_dict['in_reply_to_status_id'], tweet_dict['in_reply_to_user_id'])
        cursor.execute(postgres_insert_query, record_to_insert)
        db_connection.commit()
    postgres_select_query = "SELECT name FROM users WHERE id=%s;"
    cursor.execute(postgres_select_query, [user_dict['id']])
    result = cursor.fetchone()
    if result is not None:
        postgres_alter_query = "UPDATE users SET name = %s, screenname = %s, location = %s, description = %s, language = %s, followersnumber = %s, friendsnumber = %s WHERE id=%s;"
        record_to_alter = (user_dict['name'], user_dict['screen_name'], user_dict['location'], user_dict['description'], user_dict['lang'], user_dict['followers_count'], user_dict['friends_count'], user_dict['id'])
        cursor.execute(postgres_alter_query, record_to_alter)
    else:
        postgres_insert_query = "INSERT INTO users (id, name, screenname, location, description, language, followersnumber, friendsnumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        record_to_insert = (user_dict['id'], user_dict['name'], user_dict['screen_name'], user_dict['location'], user_dict['description'], user_dict['lang'], user_dict['followers_count'], user_dict['friends_count'])
        cursor.execute(postgres_insert_query, record_to_insert)
    db_connection.commit()
    if tweet_dict['in_reply_to_status_id'] is not None and tweet_dict['in_reply_to_user_id'] is not None:
        postgres_insert_query = "INSERT INTO comments (tweetid, userid) VALUES (%s, %s);"
        record_to_insert = (tweet_dict['in_reply_to_status_id'], tweet_dict['in_reply_to_user_id'])
        try:
            cursor.execute(postgres_insert_query, record_to_insert)
            db_connection.commit()
        except psycopg2.errors.ForeignKeyViolation:
            print('There were no user with id %s or tweet with id %s found. Row was not inserted into comments table' % (tweet_dict['in_reply_to_user_id'], tweet_dict['in_reply_to_status_id']))
            db_connection.rollback()
    if not _is_retweet(tweet_dict['text']) and len(tweet_dict['entities']['user_mentions']) > 0:
        for mentioned_user in tweet_dict['entities']['user_mentions']:
            postgres_insert_query = "INSERT INTO mentions (tweetid, userid) VALUES (%s, %s);"
            record_to_insert = (tweet_dict['id'], mentioned_user['id'])
            try:
                cursor.execute(postgres_insert_query, record_to_insert)
                db_connection.commit()
            except psycopg2.errors.ForeignKeyViolation:
                print('There were no tweet with id %s found in tweets table. Row was not inserted into mentions table' % tweet_dict['id'])
                db_connection.rollback()
    cursor.close()


def _is_retweet(text):
    return re.search("^RT @.+:", text)


def _insert_text(tweet_dict):
    if 'extended_tweet' in tweet_dict:
        full_text = tweet_dict['extended_tweet']['full_text']
    else:
        full_text = tweet_dict['text']
    return full_text


def _insert_created_at(tweet_dict):
    created_at = tweet_dict['created_at'].split()
    created_at_timestamp = created_at[5] + '_' + _insert_month_no(created_at[1]) + '_' + created_at[2] + ' ' + created_at[3]
    return created_at_timestamp


def _insert_month_no(month_str):
    month_num = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }
    return month_num.get(month_str, 'Invalid month')


def main():
    print("connected")
    conn = connect_to_database()
    update_db(conn)


if __name__ == '__main__':
    main()
