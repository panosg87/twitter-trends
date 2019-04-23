__all__ = ['Hashtag', 'HashtagPerSource', 'HashtagPerLang']

import re

from twitter_trends.base_hashtag import BaseHashtag, BaseHashtagAggregation
from twitter_trends.utils import hashtag_counts


class Hashtag(BaseHashtag):
    """Hashtag trend - responsible for creating trends for hashtags.

    Args:
        tweets_list (list): a list of tweet dictionaries.
        name (str)
    """
    def __init__(self, tweets_list, name='hashtag'):
        super().__init__(tweets_list, name)

    @staticmethod
    def _formatter(tweet):
        """Format the tweet data, by keeping only the neccessary values.

        Args:
            tweet (dict)

        Returns:
            (dict)
        """
        return {
            'id': tweet['id'],
            'created_at': tweet['created_at'],
            # MongoDB doesn't like dot in the key.
            'hashtags': [
                (ht['text'].replace('.', '_')
                 for ht in tweet['entities']['hashtags'])
            ]
        }

    def trend(self, hashtag_top_n=10):
        """Calculate the trend.

        Args:
            hashtag_top_n (int): the top n number of hashtags to return,
                defaults to 10

        Returns:
            (dict)
        """
        trends = self.count_hashtags(self.df.hashtags.values, hashtag_top_n)
        return {
            'count': trends.sum(),
            'trends': trends
        }


class HashtagPerSource(BaseHashtagAggregation):
    """Hashtag per source trend - responsible for creating trends for hashtags
    aggregating them by source.

    Args:
        tweets_list (list): a list of tweet dictionaries.
        name (str)
    """
    def __init__(self, tweets_list, name='hashtag_per_source'):
        self.column = 'source'
        super().__init__(tweets_list, name)

    def _formatter(self, tweet):
        """Format the tweet data, by keeping only the neccessary values.

        Args:
            tweet (dict)

        Returns:
            (dict)
        """
        clean = re.compile('<.*?>')
        return {
            'id': tweet['id'],
            'created_at': tweet['created_at'],
            self.column: re.sub(clean, '', tweet[self.column]),
            'hashtags': [
                (ht['text'].replace('.', '_')
                 for ht in tweet['entities']['hashtags'])
            ]
        }


class HashtagPerLang(BaseHashtagAggregation):
    """Hashtag per language trend - responsible for creating trends for
    hashtags aggregating them by language.

    Args:
        tweets_list (list): a list of tweet dictionaries.
        name (str)
    """
    def __init__(self, tweets_list, name='hashtag_per_lang'):
        self.column = 'lang'
        super().__init__(tweets_list, name)

    def _formatter(self, tweet):
        """Format the tweet data, by keeping only the neccessary values.

        Args:
            tweet (dict)

        Returns:
            (dict)
        """
        return {
            'id': tweet['id'],
            'created_at': tweet['created_at'],
            self.column: tweet[self.column],
            'hashtags': [
                (ht['text'].replace('.', '_')
                 for ht in tweet['entities']['hashtags'])
            ]
        }
