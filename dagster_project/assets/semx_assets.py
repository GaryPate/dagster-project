import tweepy
import json
import re
from datetime import datetime, timedelta
import pandas as pd
from dagster_gcp import BigQueryResource
from textblob import TextBlob
from dagster import asset
import os
from google.cloud.bigquery import LoadJobConfig, WriteDisposition

class Sentiment:

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


@asset(compute_kind="python", group_name="sentimax_compute")
def st01_tweets_to_json() -> None:
    """
    Searches the past hour of tweets
    """
    bearer_token = os.environ['BEARER_TOKEN']

    client = tweepy.Client(bearer_token)
    dt_end = datetime.now() - timedelta(hours=1)
    dt_start = datetime.now() - timedelta(hours=2)
    qry = "Bitcoin -is:retweet lang:en"
    tweets_ro = client.search_recent_tweets(query=qry
                                            , tweet_fields=['id','text','context_annotations','created_at','geo','author_id','lang','source']
                                            , expansions=["author_id", "geo.place_id"]
                                            , start_time = dt_start
                                            , end_time = dt_end
                                            , max_results=50
                                            )

    tweets_data = tweets_ro.data

    with open('/mnt/sentimax/tweet_data.json', 'w') as f:
        for tweet in tweets_data:
            print(tweet)
            f.write(json.dumps({'id': tweet.id, 'text': tweet.text}) + "\n")


@asset(compute_kind="python", group_name="sentimax_compute", deps=[st01_tweets_to_json])
def st02_tweet_json_to_bq(bigquery: BigQueryResource) -> None:
    """
    Reads JSON and loads to staging table
    """
    data = []
    with open("/mnt/sentimax/tweet_data.json", 'r', encoding='utf-8') as f:
        for line in f:
            data.append(line)

    df = pd.DataFrame(json.loads(line) for line in data)

    job_config = LoadJobConfig()
    job_config.write_disposition = (
        WriteDisposition.WRITE_TRUNCATE
    ) 

    with bigquery.get_client() as client:
        job = client.load_table_from_dataframe(
            dataframe=df,
            destination="SENTIMAX.st02_tweet_json_to_bq",
            job_config=job_config
        )
        job.result()


@asset(compute_kind="python", group_name="sentimax_compute")
def st03_calc_sentiment(st02_tweet_json_to_bq: pd.DataFrame, bigquery: BigQueryResource) -> None:
    """
    Calculates sentiment from last hour of tweets in BQ
    """

    sen = Sentiment()

    dt_load = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sentiments = []

    for index, row in st02_tweet_json_to_bq.iterrows():
        id_= row['id']
        text_ = row['text']
        clean_tweet = sen.clean_tweet(text_)
        sentiment = sen.get_tweet_sentiment(clean_tweet)
        sentiments.append([id_, text_, sentiment, dt_load])  

    df = pd.DataFrame(sentiments, columns=['id', 'text', 'sentiment', 'load_datetime'])

    job_config = LoadJobConfig()
    job_config.write_disposition = (
        WriteDisposition.WRITE_TRUNCATE
    ) 

    with bigquery.get_client() as client:
        job = client.load_table_from_dataframe(
            dataframe=df,
            destination="SENTIMAX.st03_calc_sentiment",
            job_config=job_config
        )
        job.result()
