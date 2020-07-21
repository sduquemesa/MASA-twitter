import sqlite3
import pandas as pd

DB_FILE = 'tweets.sqlite'

def get_db_data() -> pd.DataFrame:

    con = sqlite3.connect(DB_FILE)
    statement = 'SELECT * FROM tweets'
    df = pd.read_sql_query(statement, con)

    return df

if __name__ == '__main__':

    db_data = get_db_data()
    print(db_data)