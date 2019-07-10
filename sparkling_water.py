# This code was heavily adapted from code developed by GeeksForGeeks at
# https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import csv
  
class TwitterClient(object): 
    
    def __init__(self): 
        consumer_key = '************************************'
        consumer_secret = '************************************'
        access_token = '************************************'
        access_token_secret = '************************************'
  
        try: 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        tweets = []  
        try: 
            fetched_tweets = self.api.search(q = query, count = count) 
            for tweet in fetched_tweets: 
                parsed_tweet = {} 
                parsed_tweet['text'] = tweet.text 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                sval = TextBlob(self.clean_tweet(tweet.text))
                parsed_tweet['sval'] = sval.sentiment.polarity  
                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
            return tweets 
  
        except tweepy.TweepError as e: 
            print("Error : " + str(e)) 
  
def avg_sent(lst):
    return sum(lst)/len(lst)
        
def main(): 
    h2o = ['la croix', 'bubly sparkling', 'perrier', 'san pellegrino', 'spindrift', 'voss sparkling', 'klarbrunn', 'kroger sparkling', 'polar sparkling', 'dasani sparkling', 'poland spring sparkling', 'ice mountain sparkling', 'whole foods sparkling', 'wegmans sparkling']
    positive = []
    neutral = []
    negative = []
    tsentval = []
 
    for x in h2o:
        api = TwitterClient() 
        tweets = api.get_tweets(query = x, count = 200) 
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
        positive.append(100*len(ptweets)/len(tweets)) 
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
        negative.append(100*len(ntweets)/len(tweets)) 
        neutral.append(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)) 
        tsent = [tweet['sval'] for tweet in tweets]
        tsentval.append(avg_sent(tsent))
  
    sentiment = dict(zip(h2o, zip(positive, neutral, negative, tsentval)))
    with open('sparkling_water_sentiment.csv', mode='w') as file:
        writer = csv.writer(file)
        for k, v in sentiment.items():
               writer.writerow([k,v])
  
if __name__ == "__main__": 
    main() 