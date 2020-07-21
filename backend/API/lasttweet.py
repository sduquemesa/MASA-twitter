from datetime import datetime
import pandas as pd
from pathlib import Path
import sqlite3

DB_FILE = Path("../twitter_streaming/") / 'tweets.sqlite'

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def get_db_data() -> dict:

    con = sqlite3.connect(DB_FILE)
    statement = 'SELECT * FROM tweets'
    df = pd.read_sql_query(statement, con)

    return df.to_dict()

# Create a handler for our read (GET) lasttweet
def read():
    """
    This function responds to a request for /api/lasttweet
    with the tweet data

    :return:        tweet data
    """

    tweet_data = get_db_data()
    
    return dict([['{}'.format(key),tweet_data[key][0]] for key in tweet_data.keys()])