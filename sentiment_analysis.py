from textblob import TextBlob
import re


class SentimentAnalyzer:

    @staticmethod
    def get_tweet_sentiment(tweet_text):
        analysis = TextBlob(SentimentAnalyzer._clean_tweet_content(tweet_text))
        return analysis.sentiment.polarity

    @staticmethod
    def _clean_tweet_content(tweet_text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet_text).split())


def main():
    sentiment = SentimentAnalyzer()
    print(sentiment.get_tweet_sentiment("I’ve been out supporting our great @Conservatives candidates across the UK the last couple of weeks. The message on the doorstep has been clear: the British people want to get Brexit done and move our country forward #VoteConservative"))
    # print(sentiment.get_tweet_sentiment("I love it"))
    # print(sentiment.get_tweet_sentiment("I hate it"))
    # print(sentiment.get_tweet_sentiment("The best movie I've ever seen"))
    # print(sentiment.get_tweet_sentiment("The worst movie I've ever seen"))


if __name__ == '__main__':
    main()
