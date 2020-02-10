"""
Twitter 3-legged Authenticator.
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

consumer_key = 'gShAQlBULEgtI4TXbfZ9Jm67z'
consumer_secret = 'q1RaFMHXVhdARf7mWmvTJMrulUYQei6XPe1HTygX6ED4bQxpER'

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


class TwitterHandler( http.server.SimpleHTTPRequestHandler ):
    #Function to convert tweets to dataframe structure.
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        # df['id'] = np.array([tweet.id for tweet in tweets])
        # df['len'] = np.array([len(tweet.text) for tweet in tweets])
        # df['date'] = np.array([tweet.created_at for tweet in tweets])
        # df['source'] = np.array([tweet.source for tweet in tweets])
        # df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        # df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df
    
    # Function to build datafram for tweets from a specified user and put them in a specified textfile.
    def retrieve_tweets(self, api, username, filename):
        tweets = api.user_timeline(screen_name=username, count='200')
        df = self.tweets_to_data_frame(tweets)
        #print(df.head(10))
        text_file = open(filename, 'a+')
        np.savetxt(text_file, df.values,fmt='%s')
        text_file.close()
      
    def session_store( self, token ):
        self.send_header( 'Set-Cookie', 'auth={};'.format( token ) )

    def session_retrieve( self ):
        if not self.headers.get( 'Cookie' ):
            raise Exception( 'No session cookie available.' )
        
        # bit ugly, but gets token stored as dictionary from cookie
        try:
            return ast.literal_eval( self.headers.get( 'Cookie' ).split( '=' )[ 1 ] )
        except:
            # just returns it as a string
            return self.headers.get( 'Cookie' ).split( '=' )[ 1 ]

    def do_GET( self ):

        req = urllib.parse.urlparse( 'http://localhost:8080' + self.path )
        
        # return requests from Twitter go through this branch
        if req.query:
            urlnow = urllib.parse.parse_qs(req.query)
            verifier = urlnow.get("oauth_verifier")[0]
            
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            token = self.session_retrieve()
            auth.request_token = { 'oauth_token' : token,
                                     'oauth_token_secret' : verifier }
            
            try:
                auth.get_access_token(verifier)
            except tweepy.TweepError:
                print('Error! Failed to get access token.')
                
            # Prints access Token and Secret...
            print( "Access Token: {}\nAccess Token Secret: {}".format(auth.access_token,auth.access_token_secret) )
            
            
            api = tweepy.API(auth)
            # Functionality: build corpus from 200 tweets from 5 politcal candidates...
            self.retrieve_tweets(api, 'BernieSanders', 'corpus.txt')
            self.retrieve_tweets(api, 'JoeBiden', 'corpus.txt')
            self.retrieve_tweets(api, 'PeteButtigieg', 'corpus.txt')
            self.retrieve_tweets(api, 'AndrewYang', 'corpus.txt')
            self.retrieve_tweets(api, 'ewarren', 'corpus.txt')
            
            self.retrieve_tweets(api, 'FreedoniaNews', 'freedoniatweets.txt')

            exit()

        # initial requests (before the redirect to Twitter) go through this branch
        else:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret, 'http://localhost:8080')

            try:
                redirect_url = auth.get_authorization_url()
            except tweepy.TweepError:
                print('Error! Failed to get request token.')

            self.send_response( 307 )
            self.send_header('Location', redirect_url)
            self.session_store(auth.request_token['oauth_token'])
            self.end_headers()


def run( server_class = http.server.HTTPServer, handler_class = TwitterHandler ):
    server_address = ( 'localhost', 8080 )
    httpd = server_class( server_address, handler_class )
    httpd.serve_forever()


if __name__ == '__main__':
    run()
