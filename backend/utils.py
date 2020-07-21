"""Some helper functions



@Author: Sebastian Duque Mesa

"""

import numpy as np
import pandas as pd

def parse_tweet(tweet: dict) ->  dict:
    '''Parse tweet's data and store to pandas dataframe'''

    # Parse tweet's root level info
    tweet_id_str = tweet['id_str']
    tweet_created_at = tweet['created_at']

    # Tweet's user data
    tweet_username = tweet['user']['screen_name']
    tweet_user_id = tweet['user']['id_str']
    tweet_user_location = tweet['user']['location']

    # Tweet's geo data
    if 'coordinates' in tweet:
        tweet_coords = tweet['coordinates']      # Tweet coordinates in [long,lat]
    elif 'place' in tweet:
        tweet_bounding_box = tweet['place']['bounding_box']['coordinates']      # Tweet's location bounding box
        tweet_coords = bbox_centroid(tweet_bounding_box)                  # Tweet's centroid
    else:
        tweet_coords = None

    tweet_data = {
        'id': tweet_id_str,
        'coords': tweet_coords
    }

    return tweet_data

def bbox_centroid(bounding_box: list) -> list:
    '''Calculates the centroid of a bounding box'''

    # list of unique bbox longitudes
    longs = np.unique( [point[0] for point in bounding_box])
    # list of unique bbox latitudes
    lats =  np.unique( [point[1] for point in bounding_box])
    
    # Centroid is the average of longs and lats
    centroid_long = np.sum(longs)/2
    centroid_lat = np.sum(lats)/2

    return [centroid_long,centroid_lat]