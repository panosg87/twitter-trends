#!/usr/bin/env bash

airflow initdb

AIRFLOW_HOME=$1
TWIITER_CONSUMER_KEY=$2
TWITTER_CONSUMER_SECRET=$3
TWITTER_OAUTH_TOKEN=$4
TWITTER_OAUTH_TOKEN_SECRET=$5

airflow variables -s TWITTER_CONSUMER_KEY $TWIITER_CONSUMER_KEY
airflow variables -s TWITTER_CONSUMER_SECRET $TWITTER_CONSUMER_SECRET
airflow variables -s TWITTER_OAUTH_TOKEN $TWITTER_OAUTH_TOKEN
airflow variables -s TWITTER_OAUTH_TOKEN_SECRET $TWITTER_OAUTH_TOKEN_SECRET

cp $AIRFLOW_HOME/twitter-trends/airflow_pipelines/twitter_trends_pipeline.py $AIRFLOW_HOME/dags/
cp -r $AIRFLOW_HOME/twitter-trends/airflow_pipelines/twitter_trends/ $AIRFLOW_HOME/dags/

airflow scheduler &
airflow webserver
