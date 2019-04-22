import datetime

import tweepy as tw


class TwitterParser:

    def __init__(self, api, client, db, collection):
        self.api = api
        # Keep track of state
        self.client = client
        self.db = db
        self.collection = collection

    #TODO: Do not implement, but explain.
    def _state_check(self):
        return False

    @staticmethod
    def _parsing_end_dt(start_datetime, hrs_before):
        return start_datetime - datetime.timedelta(hours=hrs_before)

    def tweet_cursor(self, max_id, geocode, parsing_end_dt):
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

        max_id = None
        if self._state_check():
            # modify end date
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
    count = 0

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(oauth_token, oauth_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    parser = TwitterParser(api, client, db, state_collection)
    for twx in parser.parse(geocode, hrs_before):

        twx['_id'] = twx['id']

        try:
            client[db][collection].insert_one(twx)
        except Exception as e:
            print('Occured while saving...', e)

        count += 1
        if count % 10000 == 0:
            # Sort of progress indication.
            print("Saved... ", count)
