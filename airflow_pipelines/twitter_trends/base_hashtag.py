import pandas as pd

from twitter_trends.utils import hashtag_counts


class BaseHashtag:
    """Base class for the trends that provides abstraction level of
    functionality that will be used by child classes as well.

    Args:
        tweets_list (list):
        name (str):
    """
    def __init__(self, tweets_list, name):
        self.df = pd.DataFrame(self.format_tweet_data(tweets_list))
        self.name = name

    def format_tweet_data(self, tweets):
        """Format the tweets in a specific format.

        Args:
            tweets (list):

        Returns:
            data (list):
        """
        data = []
        for tweet in tweets:
            try:
                fmt_tw = self._formatter(tweet)
            except:
                # TODO: add logging
                continue

            data.append(fmt_tw)
        return data

    @staticmethod
    def count_hashtags(hashtags, top_n=None):
        """Count the values of the hashtags.

        Args:
            hashtags (list):
            top_n (int / None):
        """
        return hashtag_counts(hashtags)[:top_n].to_dict()

    def trend(self, **kwargs):
        raise NotImplementedError


class BaseHashtagAggregation(BaseHashtag):
    """Provides another level of abstraction for calculation of trends that
    need specific aggergation count of hashtags.
    """
    def _get_top_values_from_column(self):
        """Aggregate by a specific column and return the values in descending
        sorting.

        Returns:
            (pd.Series): top n values for this column.
        """
        return self.df.groupby(
            self.column
        )['id'].count().sort_values(ascending=False).reset_index()

    def trend(self, hashtag_top_n, column_top_n):
        """Calculate and return a trend.

        Args:
            hashtags_top_n (int): top n hashtags to show.
            column_top_n (int): top n column key to show.

        Returns:
            trends (dict)
        """
        trend = {}

        top_values = self._get_top_values_from_column()

        for s_dict in top_values[:column_top_n].to_dict('records'):

            # MongoDB doesn't like dot in the key of a document..
            trend[s_dict[self.column].replace('.', '_')] = {
                'count': s_dict['id'],
                'trends': self.count_hashtags(
                    (self.df[self.df[self.column] ==
                            s_dict[self.column]].hashtags.values),
                    hashtag_top_n
                )
            }

        return trend
