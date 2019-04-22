def controller(trend_obj, extra):

    if trend_obj.name == 'hashtag':

        return trend_obj.trend(hashtag_top_n=extra.get('hashtag_top_n', 10))

    if trend_obj.name  in ('hashtag_per_source', 'hashtag_per_lang'):

        return trend_obj.trend(hashtag_top_n=extra.get('hashtag_top_n', 10),
                               column_top_n=extra.get('column_top_n', 3))
