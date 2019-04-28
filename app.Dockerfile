FROM ubuntu:bionic

ENV DEBIAN_FRONTEND=noninteractive

ENV AIRFLOW_HOME=/root/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

RUN apt-get update -q && apt-get install -yq \
    python3-dev \
    python3-pip \
    git \
    && apt-get autoclean -y

RUN pip3 install apache-airflow==1.10.3

WORKDIR $AIRFLOW_HOME/

RUN git clone https://github.com/panosg87/twitter-trends.git
RUN pip3 install -r $AIRFLOW_HOME/twitter-trends/airflow_pipelines/requirements.txt

RUN mkdir dags

COPY start_airflow.sh .
RUN chmod +x start_airflow.sh

EXPOSE 8080

CMD ./start_airflow.sh $AIRFLOW_HOME \
$TWITTER_CONSUMER_KEY $TWITTER_CONSUMER_SECRET \
$TWITTER_OAUTH_TOKEN $TWITTER_OAUTH_TOKEN_SECRET
