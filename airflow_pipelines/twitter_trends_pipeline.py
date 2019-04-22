import datetime
import os

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from pymongo import MongoClient

from twitter_trends import calculate_trends
from twitter_trends.parse_data import parse_tweet_data

client = MongoClient()
db = client['twitter']

default_args = {
    'owner': 'panosg',
    'start_date': datetime.datetime(2019, 4, 23),
    'retries': 1,
    'retry_delay': datetime.timedelta(seconds=20)
}

parsing_kwargs = {
    'consumer_key': Variable.get('TWITTER_CONSUMER_KEY'),
    'consumer_secret': Variable.get('TWITTER_CONSUMER_SECRET'),
    'oauth_token': Variable.get('TWITTER_OAUTH_TOKEN'),
    'oauth_token_secret': Variable.get('TWITTER_OAUTH_TOKEN_SECRET'),
    'db': 'twitter-data',
    'collection': 'raw-tweets',
    'state_collection': 'state',
    'client': client,
    'hrs_before': 72,
    'geocode': '52.378,4.9,10km'  # Amsterdam area
}

hashtags_kwargs = {
    'trend_type': 'hashtag',
    'db': 'twitter-data',
    'source_collection': 'raw-tweets',
    'target_collection': 'hashtag',
    'client': client,
    'extras': {
        'hashtag_top_n': 100
    }
}

hashtags_per_source_kwargs = {
    'trend_type': 'hashtag_per_source',
    'db': 'twitter-data',
    'source_collection': 'raw-tweets',
    'target_collection': 'hashtag-per-source',
    'client': client,
    'extras': {
        'hashtag_top_n': 100,
        'column_top_n': 10
    }
}

hashtags_per_lang_kwargs = {
    'trend_type': 'hashtag_per_lang',
    'db': 'twitter-data',
    'source_collection': 'raw-tweets',
    'target_collection': 'hashtag-per-lang',
    'client': client,
    'extras': {
        'hashtag_top_n': 100,
        'column_top_n': 10
    }
}

with DAG('twitter-trends', default_args=default_args) as dag:

    parse_data = PythonOperator(
        task_id='parse_data',
        python_callable=parse_tweet_data,
        op_kwargs=parsing_kwargs,
        execution_timeout=datetime.timedelta(hours=3)
    )

    calc_hashtags = PythonOperator(
        task_id='calculate_hashtags',
        python_callable=calculate_trends.calculate,
        op_kwargs=hashtags_kwargs,
        execution_timeout=datetime.timedelta(minutes=5)
    )

    calc_hashtags_per_source = PythonOperator(
        task_id='calculate_hashtags_per_source',
        python_callable=calculate_trends.calculate,
        op_kwargs=hashtags_per_source_kwargs,
        execution_timeout=datetime.timedelta(minutes=5)
    )

    calc_hashtags_per_lang = PythonOperator(
        task_id='calculate_hashtags_per_lang',
        python_callable=calculate_trends.calculate,
        op_kwargs=hashtags_per_lang_kwargs,
        execution_timeout=datetime.timedelta(minutes=5)
    )

parse_data >> calc_hashtags >> calc_hashtags_per_source >> calc_hashtags_per_lang
