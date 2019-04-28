import datetime
import os

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from pymongo import MongoClient

from twitter_trends import calculate_trends
from twitter_trends.parse_data import parse_tweet_data

HOST = os.environ.get('MONGODB_HOST')
HRS_BEFORE = 72

client = MongoClient(host=HOST)

default_args = {
    'owner': 'panosg',
    'start_date': datetime.datetime(2019, 4, 23),
    'retries': 1,
    'retry_delay': datetime.timedelta(seconds=20),
    'client': client,
    'db': 'twitter-data'
}

parsing_kwargs = {
    'consumer_key': Variable.get('TWITTER_CONSUMER_KEY'),
    'consumer_secret': Variable.get('TWITTER_CONSUMER_SECRET'),
    'oauth_token': Variable.get('TWITTER_OAUTH_TOKEN'),
    'oauth_token_secret': Variable.get('TWITTER_OAUTH_TOKEN_SECRET'),
    'client': client,
    'db': 'twitter-data',
    'collection': 'raw-tweets',
    'state_collection': 'state',
    'hrs_before': HRS_BEFORE,
    'geocode': '52.378,4.9,10km'  # Amsterdam area
}

hashtags_kwargs = {
    'trend_type': 'hashtag',
    'client': client,
    'db': 'twitter-data',
    'source_collection': 'raw-tweets',
    'target_collection': 'hashtag',
    'extras': {
        'hashtag_top_n': 100
    }
}

hashtags_per_source_kwargs = {
    'trend_type': 'hashtag_per_source',
    'client': client,
    'db': 'twitter-data',
    'source_collection': 'raw-tweets',
    'target_collection': 'hashtag-per-source',
    'extras': {
        'hashtag_top_n': 100,
        'column_top_n': 10
    }
}

hashtags_per_lang_kwargs = {
    'trend_type': 'hashtag_per_lang',
    'client': client,
    'db': 'twitter-data',
    'source_collection': 'raw-tweets',
    'target_collection': 'hashtag-per-lang',
    'extras': {
        'hashtag_top_n': 100,
        'column_top_n': 10
    }
}

calc_dags_payload = [
    ('calculate_hashtags', hashtags_kwargs),
    ('calculate_hashtags_per_source', hashtags_per_source_kwargs),
    ('calculate_hashtags_per_lang', hashtags_per_lang_kwargs)
]

calc_dags = []

with DAG('twitter-trends', default_args=default_args) as dag:

    parse_data = PythonOperator(
        task_id='parse_data',
        python_callable=parse_tweet_data,
        op_kwargs=parsing_kwargs,
        execution_timeout=datetime.timedelta(hours=5)
    )

    for w in calc_dags_payload:
        calc_dags.append(PythonOperator(
            task_id=w[0],
            python_callable=calculate_trends.calculate,
            op_kwargs=w[1],
            execution_timeout=datetime.timedelta(minutes=5)
        ))

    parse_data >> calc_dags
