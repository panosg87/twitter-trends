import os

from twitter_trends.trend_controller import controller
from twitter_trends.trend_factory import factory
from twitter_trends.utils import get_tweets


def calculate(client, db, source_collection, target_collection, trend_type,
              extras):

    # Fail in case the class is not implemented.
    cls = factory(trend_type)

    tweets = get_tweets(client, db, source_collection)

    trend = cls(tweets)
    output = controller(trend, extras)

    client[db][target_collection].insert_one(output)
