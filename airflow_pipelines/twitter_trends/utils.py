import pandas as pd


def hashtag_counts(hashtags):
    """Count values of hashtags.

    Args:
        hashtahs (iter): an iter (list / np.array) of iter, that holds the
            hashtags.

    Returns:
        (pd.Series): the hashtags and the counts of them.
    """
    return pd.Series([
        ht.lower() for list_ in hashtags for ht in list_
    ]).value_counts()


def get_tweets(client, db, collection):
    """Load tweets from the database.

    Args:
        client (pymongo.MongoClient)
        db (str)
        collection (str)
    """
    return list(client[db][collection].find())
