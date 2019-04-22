import pandas as pd

from twitter_trends.utils import hashtag_counts


class BaseHashtag:

    def __init__(self, tweets_list, name):
        self.df = pd.DataFrame(self.format_tweet_data(tweets_list))
        self.name = name

    def format_tweet_data(self, tweets):
        data = []

        for tweet in tweets:
            try:
                # Formatted tweet.
                fmt_tw = self._formatter(tweet)
            except:
                # TODO: log
                continue

            data.append(fmt_tw)
        return data

    @staticmethod
    def count_hashtags(hashtags, top_n=None):
        return hashtag_counts(hashtags)[:top_n].to_dict()

    def trend(self, **kwargs):
        raise NotImplementedError


class BaseHashtagAggregation(BaseHashtag):

    def _get_top_values_from_column(self):
        return self.df.groupby(
            self.column
        )['id'].count().sort_values(ascending=False).reset_index()

    def trend(self, hashtag_top_n, column_top_n):
        trend = {}

        top_values = self._get_top_values_from_column()

        for s_dict in top_values[:column_top_n].to_dict('records'):

            # MongoDB doesn't like dot in the key.
            trend[s_dict[self.column].replace('.', '_')] = {
                'count': s_dict['id'],
                'trends': self.count_hashtags(
                    (self.df[self.df[self.column] == 
                            s_dict[self.column]].hashtags.values),
                    hashtag_top_n
                )
            }

        return trend
