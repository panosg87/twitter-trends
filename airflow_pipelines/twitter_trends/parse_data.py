import datetime

import tweepy as tw


class TwitterParser:
    """Serves as the main functionality for parsing tweets.

    Args:
        api (tw.API): authorised connector with the Twitter Stream.
        client (pymongo.MongoClient)
        db (str)
        collection (str)
    """

    def __init__(self, api, client, db, collection):
        self.api = api
        self.client = client
        self.db = db
        self.collection = collection

    def _state_check(self):
        """This method is not implemented but the main idea behind it would be
        to check the state of this particular job. For example, if the parsing
        fails for some reason, as some point in time, the application should
        be able to recover from this point and not re-collect information.

        Moreover, this method would be closely related with the logic of
        the parsing point that this job should reach.
        """
        return False

    @staticmethod
    def _parsing_end_dt(start_datetime, hrs_before):
        """Get the parsing end datetime.

        Args:
            start_datetime (datetime.datetime)
            hrs_before (int)

        Returns:
            (datetime.datetime): parsing end datetime.
        """
        return start_datetime - datetime.timedelta(hours=hrs_before)

    def tweet_cursor(self, max_id, geocode, parsing_end_dt):
        """Generates tweets from the Twitter Stream.

        The Standard API of Twitter has certain limitations. Using this Cursos
        class, when we reach the request limit, it will auto-wait until we
        are able (15 minutes later) to get tweets again.

        Args:
            max_id (int): relates to parsing state.
            geocode (str): geo location attrs.
            parsing_end_dt (datetime.datetime): end parsing datetime.

        Yields:
            tweet (tw.Tweet):
        """
        tweets = tw.Cursor(self.api.search,
                           search_words='',  # Search for nothing.
                           geocode=geocode,
                           result_type="recent",
                           count=100,
                           max_id=max_id + 1 if max_id else max_id,
                           tweet_mode="extended").items()

        for tweet in tweets:
            if tweet.created_at > parsing_end_dt:
                yield tweet
            else:
                break

    def parse(self, geocode, hrs_before):
        """Parse - collect tweets.

        Args:
            geocode (str): geo attributes of the location.
            hrs_before (int): collect data until hours before.

        Yields:
            (dict): tweet data in dictionary format.
        """
        max_id = None
        if self._state_check():
            # modify end parsing d date - related to parsing state.
            pass

        start_dt = datetime.datetime.now()
        parsing_end_dt = self._parsing_end_dt(start_dt, hrs_before)
        for tweet in self.tweet_cursor(max_id, geocode, parsing_end_dt):
            yield tweet._json


def parse_tweet_data(consumer_key,
                     consumer_secret,
                     oauth_token,
                     oauth_token_secret,
                     hrs_before,
                     geocode,
                     client,
                     db,
                     collection,
                     state_collection):

    """Parse tweet data and stores them to the database.

    The main function that contains all the neccessary logic in order to:
        - connect to a Twitter Stream
        - collect tweets
        - store tweets

    Args:
        consumer_key (str):
        consumer_secret (str):
        oauth_token (str):
        oauth_token_secret (str):
        hrs_before (int): until how many hours before should collect data.
        geocode (str): geo location attrs.
        client (pymongo.MongoClient): MongoDB client
        db (str): database name.
        collection (str): collection name.
        state_collection (str): collection name of the place that the state
            of the pipeline would store it's state. Is not been used.
    """
    count = 0

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(oauth_token, oauth_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    parser = TwitterParser(api, client, db, state_collection)
    for twx in parser.parse(geocode, hrs_before):

        # Automatically index tweets.
        twx['_id'] = twx['id']

        try:
            client[db][collection].insert_one(twx)
        except Exception as e:
            print('Occured while saving...', e)

        count += 1
        if count % 10000 == 0:
            # Sort of progress indication.
            print("Saved... ", count)
