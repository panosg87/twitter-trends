__all__ = ['Hashtag', 'HashtagPerSource', 'HashtagPerLang']

import re

from twitter_trends.base_hashtag import BaseHashtag, BaseHashtagAggregation
from twitter_trends.utils import hashtag_counts


class Hashtag(BaseHashtag):

    def __init__(self, tweets_list, name='hashtag'):
        super().__init__(tweets_list, name)

    @staticmethod
    def _formatter(tweet):
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
        return self.count_hashtags(self.df.hashtags.values, hashtag_top_n)


class HashtagPerSource(BaseHashtagAggregation):

    def __init__(self, tweets_list, name='hashtag_per_source'):
        self.column = 'source'
        super().__init__(tweets_list, name)

    def _formatter(self, tweet):
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

    def __init__(self, tweets_list, name='hashtag_per_lang'):
        self.column = 'lang'
        super().__init__(tweets_list, name)

    def _formatter(self, tweet):
        return {
            'id': tweet['id'],
            'created_at': tweet['created_at'],
            self.column: tweet[self.column],
            'hashtags': [
                (ht['text'].replace('.', '_')
                 for ht in tweet['entities']['hashtags'])
            ]
        }
