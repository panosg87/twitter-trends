#!/bin/bash
sudo apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -yq

# Python stuff
sudo add-apt-repository ppa:jonathonf/python-3.6 -y
sudo apt-get update -y
sudo apt-get install python3.6 -y
curl https://bootstrap.pypa.io/get-pip.py | sudo -H python3.6
sudo apt-get install python3.6-dev -y

sudo apt-get install -y python3 python3-dev
sudo apt-get install -y python-pip
sudo apt-get install -y libssl-dev libffi-dev
sudo apt-get install -y libxml2-dev libxslt1-dev

export LC_ALL=C

git clone https://github.com/panosg87/twitter-trends.git
sudo pip3.6 install -r ~/twitter-trends/airflow_pipelines/requirements.txt

# MongoDB configuration
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
sudo service mongod start

# Airflow configuration
sudo pip3.6 install apache-airflow
export AIRFLOW_HOME=~/airflow

airflow initdb

airflow variables -s TWITTER_CONSUMER_KEY $1
airflow variables -s TWITTER_CONSUMER_SECRET $2
airflow variables -s TWITTER_OAUTH_TOKEN $3
airflow variables -s TWITTER_OAUTH_TOKEN_SECRET $4

mkdir ~/airflow/dags
cp -r ~/twitter-trends/airflow_pipelines/twitter_trends ~/airflow/dags/
cp ~/twitter-trends/airflow_pipelines/twitter_trends_pipeline.py ~/airflow/dags/

nohup airflow scheduler >> ~/airflow/logs/scheduler.logs &
nohup airflow webserver -p 8080 $* >> ~/airflow/logs/webserver.logs &
