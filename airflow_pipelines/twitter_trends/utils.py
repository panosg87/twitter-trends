import pandas as pd


def hashtag_counts(hashtags):
    return pd.Series([
        ht.lower() for list_ in hashtags for ht in list_
    ]).value_counts()


def get_tweets(client, db, collection):
    return list(client[db][collection].find())
