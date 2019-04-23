from twitter_trends.hashtags import *

TREND_MAP = {
    'hashtag': Hashtag,
    'hashtag_per_source': HashtagPerSource,
    'hashtag_per_lang': HashtagPerLang
}


def factory(trend_type):
    """Factory function, responsible for returning different classes of trends.

    Args;
        trend_type (str): the type of class.

    Returnds:
        cls (base_hashtags.BaseHashtag): a subclass of this base class.
    """
    try:
        cls = TREND_MAP[trend_type]
    except:
        raise Exception('Trend type {} is not valid...'.format(trend_type))

    return cls
