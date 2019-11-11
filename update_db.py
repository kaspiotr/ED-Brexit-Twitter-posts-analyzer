import psycopg2
import jsonlines
import os
import glob


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


def insert_into_db(db_connection, tweet_dict):
    cursor = db_connection.cursor()
    full_text = _insert_text(tweet_dict)
    created_at = _insert_created_at(tweet_dict)
    postgres_insert_query = "INSERT INTO tweets (id, userid, fulltext, createdat, inreplytotweetid, inreplytouserid) VALUES (%s, %s, %s, %s, %s, %s);"
    record_to_insert = (tweet_dict['id'], tweet_dict['user']['id'], full_text, created_at, tweet_dict['in_reply_to_status_id'], tweet_dict['in_reply_to_user_id'])
    cursor.execute(postgres_insert_query, record_to_insert)
    user_dict = tweet_dict['user']
    postgres_insert_query = "INSERT INTO users (id, name, screenname, location, description, language, followersnumber, friendsnumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    record_to_insert = (user_dict['id'], user_dict['name'], user_dict['screen_name'], user_dict['location'], user_dict['description'], user_dict['lang'], user_dict['followers_count'], user_dict['friends_count'])
    cursor.execute(postgres_insert_query, record_to_insert)


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
    conn = connect_to_database()
    print("connected")
    update_db(conn)


if __name__ == '__main__':
    main()
