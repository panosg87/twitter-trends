#!/usr/bin/env bash

airflow initdb

AIRFLOW_HOME=$1

airflow variables -s TWITTER_CONSUMER_KEY $2
airflow variables -s TWITTER_CONSUMER_SECRET $3
airflow variables -s TWITTER_OAUTH_TOKEN $4
airflow variables -s TWITTER_OAUTH_TOKEN_SECRET $5

cp $AIRFLOW_HOME/twitter-trends/airflow_pipelines/twitter_trends_pipeline.py $AIRFLOW_HOME/dags/
cp -r $AIRFLOW_HOME/twitter-trends/airflow_pipelines/twitter_trends/ $AIRFLOW_HOME/dags/

airflow scheduler &
airflow webserver
