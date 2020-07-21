"""Defines the listener class passed to tweepy


@Author: Sebastian Duque Mesa

"""

from tweepy.streaming import StreamListener
from tweepy.api import API
import json
import time
import sys
import pandas as pd
from sqlalchemy import create_engine
from utils import parse_tweet

class Listener(StreamListener):
    """ 
    A listener that handles tweets received from the stream.
    """
    def __init__(self, api = None):
        self.api = api or API(wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.reconnection_attemps = 0
        self.collected_tweets = 0

        # create a engine to the database
        # self.engine = create_engine('sqlite:///app/tweets.sqlite')
        # switch to the following definition if run this code locally
        self.engine = create_engine('sqlite:///tweets.sqlite')

    def on_status(self, status):
        """Called when a new status arrives
        Recieves a Status object. 
        Tweet data is in Status._json which is already a dict.

        """

        self.reconnection_attemps = 0       # restart reconnection attemps counter when there is incoming data
        self.collected_tweets += 1

        tweet = status._json
        tweet_data = parse_tweet(tweet)

        try:
            tweet_embed_data = self.api.get_oembed(tweet_data['id'])
            tweet_html = tweet_embed_data['html'].strip()
        except:
            return True

        # append html data to dict
        tweet_data['html'] = tweet_html

        # convert into dataframe
        df = pd.DataFrame(tweet_data, index=[0])
        # convert string of time into date time obejct
        df['created_at'] = pd.to_datetime(df.created_at)

        # push tweet into database
        df.to_sql('tweets', con=self.engine, if_exists='replace')

        # print(json.dumps(tweet_data, indent=4, sort_keys=True))

        return True

    def on_error(self, status):
        """Called when a non-200 status code is returned
        Handles rate limit, increses reconnection attempt time every time is unsuccessful.
        """
        
        if status == 420:
            self.reconnection_attemps += 1
            sys.stdout.write('Error 420: Enhance Your Calm, the app has been rate limited\n')
            time.sleep(60*self.reconnection_attemps)
            return True
        else:
            sys.stdout.write('Error {}\n'.format(status))
            return False
