import tweepy
import pyodbc


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
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    # connection with database
    driver = "ODBC Driver 17 for SQL Server"
    server = "tcp:brexitanalyzer.database.windows.net"
    database = "BrexitTweetsDB"
    username = "BrexitAnalyzer"
    password = "EDzespol5"

    connection_string = 'DRIVER={driver};PORT=1433;SERVER={server};DATABASE={database};UID={username};PWD={password}'.format(driver=driver, server=server, database=database, username=username, password=password)
    conn = pyodbc.connect(connection_string)

    print("connected")
    cursor = conn.cursor()


if __name__ == '__main__':
    main()
