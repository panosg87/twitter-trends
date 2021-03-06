def controller(trend_obj, extra):
    """Responsible for the calculation of the trends by providing each
    trend instance with the appropriate input.

    Args:
        trend_obj (base_hashtag.BaseHashtag): an object of one of the
            subclasses.
        extra (dict): extra information for each trend object.

    Returns:
        (dict): returns the result of the trends calculated.
    """
    if trend_obj.name == 'hashtag':

        return trend_obj.trend(hashtag_top_n=extra.get('hashtag_top_n', 10))

    if trend_obj.name  in ('hashtag_per_source', 'hashtag_per_lang'):

        return trend_obj.trend(hashtag_top_n=extra.get('hashtag_top_n', 10),
                               column_top_n=extra.get('column_top_n', 3))
