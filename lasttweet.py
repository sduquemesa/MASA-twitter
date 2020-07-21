from datetime import datetime
import pandas as pd
from pathlib import Path
import sqlite3

DB_FILE = Path("./") / 'tweets.sqlite'

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def get_db_data() -> pd.DataFrame:

    con = sqlite3.connect(DB_FILE)
    statement = 'SELECT * FROM tweets'
    df = pd.read_sql_query(statement, con)

    return df

# Create a handler for our read (GET) lasttweet
def read():
    """
    This function responds to a request for /api/lasttweet
    with the tweet data

    :return:        tweet data
    """

    tweet_data = get_db_data()
    api_data_dict = {
        'created_at': tweet_data['created_at'][0],
        'fetched_at': get_timestamp(),
        'coords': tweet_data['coords'][0],
        'html_data': tweet_data['html'][0]
    }
    
    return api_data_dict