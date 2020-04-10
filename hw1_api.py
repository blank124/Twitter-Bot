"""
Twitter bot to post tweets to Freedonia based on sentiment.
@author: michaelblank
"""
import http.server
import http.client
import urllib.parse
import ast
import tweepy
import json
import numpy as np
import pandas as pd
import gpt_2_simple as gpt2
import os
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import botometer
import re

consumer_key = 'XXXXXXXXXX'
consumer_secret = 'XXXXXXXXXX'
access_token = 'XXXXXXXXXX'
access_secret = 'XXXXXXXXXX'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

def tweet_reply(api, username):
    tweets = api.user_timeline(screen_name=username, count='8')
    
    df = tweets_to_data_frame(tweets)
    
    tweets_array = []
    tweets_ids = []
    for tweet in df.values:
        tweets_array.append(tweet[0])
    for tweet_id in df.id:
        tweets_ids.append(tweet_id)

    #Uncomment if you wish to train GPT.
    #sess = train_GPT()

    #Uncomment if you wish to run GPT without training.
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)
    
    sid_obj = SentimentIntensityAnalyzer()
    positioninidlist = 0
    for tweet in tweets_array:
        tweet_subject = ''
        support_tweet = ''
        sentiment_dict = sid_obj.polarity_scores(tweet)
        
        if sentiment_dict['compound'] >= 0.05 : 
            tweet_sentiment = 'Positive'
  
        elif sentiment_dict['compound'] <= - 0.05 : 
            tweet_sentiment = 'Negative'
        
        if 'Sylvania' in tweet:
            tweet_subject = 'Sylvania'
            needed_sentiment = 'Positive'
            if tweet_sentiment is 'Negative':
                support_tweet = 'False'
            else:
                support_tweet = 'True'
        
        elif 'Ambassador Trentino' in tweet:
            tweet_subject = 'Ambassador Trentino'
            needed_sentiment = 'Positive'
            if tweet_sentiment is 'Negative':
                support_tweet = 'False'
            else:
                support_tweet = 'True'
        
        elif 'Freedonia' in tweet:
            tweet_subject = 'Freedonia'
            needed_sentiment = 'Negative'
            if tweet_sentiment is 'Negative':
                support_tweet = 'True'
            else:
                support_tweet = 'False'
        
        elif 'Rufus T. Firefly' in tweet:
            tweet_subject = 'Rufus T. Firefly'
            needed_sentiment = 'Negative'
            if tweet_sentiment is 'Negative':
                support_tweet = 'True'
            else:
                support_tweet = 'False'

        generated_text = ''
        generated_sentiment = ''
        
        while generated_sentiment != needed_sentiment:
            if support_tweet == 'True':
                generated_text = gpt2.generate(sess, return_as_list=True, length = 35, prefix=tweet_subject)[0]
            elif support_tweet == 'False':
                generated_text = gpt2.generate(sess, return_as_list=True, length = 35, prefix=tweet_subject)[0]

            
            generated_sentiment_dict = sid_obj.polarity_scores(generated_text)

            if generated_sentiment_dict['compound'] >= 0.05 : 
                generated_sentiment = 'Positive'
    
            elif generated_sentiment_dict['compound'] <= - 0.05 : 
                generated_sentiment = 'Negative'

        #Uncomment below if you wish to see the tweet before posting.
        """ print("GPT generated tweet...\n")
        print(generated_text)
        print("\n") """

        #Uncomment below if you wish to post reply tweets to all 8 tweets on FreedoniaNews.
        generated_text = '@FreedoniaNews ' + generated_text
        generated_text = re.sub(r'^https?:\/\/.*[\r\n]*', '', generated_text, flags=re.MULTILINE)
        generated_text = re.sub(r'http\S+', '', generated_text)
        api.update_status(generated_text,in_reply_to_status_id = tweets_ids[positioninidlist])
        positioninidlist = positioninidlist + 1
        
def botometer_runner():
    twitter_app_auth = {
    'consumer_key': 'gShAQlBULEgtI4TXbfZ9Jm67z',
    'consumer_secret': 'q1RaFMHXVhdARf7mWmvTJMrulUYQei6XPe1HTygX6ED4bQxpER',
    'access_token': '1222181578144735232-LpfSW1TE087zQ1PG15ZdpTS7PHZ8CO',
    'access_token_secret': 'wAPpFATXBwjkkj4zsO6BXx1cLRdaC3ro7uKlg6Hgt665e',
    }
    bom = botometer.Botometer(wait_on_ratelimit=True, rapidapi_key='ce5f75383amsh42cdd089b1d0381p12d498jsn8f456fa3f36b', **twitter_app_auth)
    result = bom.check_account('@Michaelblank123')
    return result


def tweets_to_data_frame(tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        return df


def train_GPT():
    model_name = "124M"
    if not os.path.isdir(os.path.join("models", model_name)):
        print(f"Downloading {model_name} model...")
        gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/
    
    file_name = "corpus.txt"
    sess = gpt2.start_tf_sess()
    gpt2.finetune(sess,file_name,model_name=model_name,steps=1)   # steps is max number of training steps

    return sess

if __name__ == '__main__':
    api = tweepy.API(auth)

    # Uncomment to reply to FreedoniaNews tweets.
    #tweet_reply(api, 'FreedoniaNews')

    # Uncomment to print Botometer results.
    #print(botometer_runner())

    

