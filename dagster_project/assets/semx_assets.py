import tweepy
import json
import os
from datetime import datetime, timedelta
import pandas as pd
from dagster_gcp import BigQueryResource
import re
from textblob import TextBlob
from dagster_gcp import BigQueryResource
import pandas as pd
from dagster import asset, AssetIn


@asset(compute_kind="python", group_name="sentimax")
def st01_tweets_to_json():
    """
    Searches the past hour of tweets
    """
    bearer_token = os.environ['BEARER_TOKEN']
    client = tweepy.Client(bearer_token)
    dt_end = datetime.now() - timedelta(hours=1)
    dt_start = datetime.now() - timedelta(hours=2)
    qry = "Bitcoin"
    tweets_ro = client.search_recent_tweets(query=qry
                                            , tweet_fields=['id','text','context_annotations','created_at','geo','author_id','lang','source']
                                            , expansions=["author_id", "geo.place_id"]
                                            , start_time = dt_start
                                            , end_time = dt_end
                                            , max_results=10
                                            )

    tweets_data = tweets_ro.data

    with open('tweet_data.json', 'w') as f:
        for tweet in tweets_data:
            print(tweet)
            f.write(json.dumps({'id': tweet.id, 'text': tweet.text}) + "\n")


@asset(compute_kind="python", group_name="sentimax")
def st02_tweet_json_to_bq(bigquery: BigQueryResource, st01_tweets_to_json) -> None:
    """
    Reads JSON and loads to staging table
    """
    data = []
    with open("data/tweet_data.json", 'r', encoding='utf-8') as f:
        for line in f:
            data.append(line)

    df = pd.DataFrame(json.loads(line) for line in data)

    with bigquery.get_client() as client:
        job = client.load_table_from_dataframe(
            dataframe=df,
            destination="SENTIMAX.tweet_data_staging",
        )
        job.result()


class Sentiment:

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
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


# @asset(
#     key_prefix=["semx_stg03_tweet_increment"]  # will be used as the dataset in BigQuery
# )
# def my_table() -> pd.DataFrame:  # the name of the asset will be the table name
#     ...

# defs = Definitions(
#     assets=[my_table],
#     resources={
#         "io_manager": BigQueryPandasIOManager(project=EnvVar("GCP_PROJECT"))
#     }
# )



@asset(
    compute_kind="python",
    group_name="sentimax",
    #deps=get_asset_key_for_model([dagster_dbt_assets], "semx_stg03_tweet_increment"),
    ins={"tweet_history": AssetIn("semx_stg03_tweet_increment")}
)
def st04_calc_sentiment(bigquery: BigQueryResource, tweet_history: pd.DataFrame) -> None:
    """
    Calculates sentiment from last hour of tweets in BQ
    """

    sen = Sentiment()

    #data = []

    dt_load = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # with open("tweet_data.json", 'r', encoding='utf-8') as f:
    #     for line in f:
    #         data.append(json.loads(line))

    sentiments = []

    for index, row in tweet_history.iterrows():
        id_= row['id']
        text_ = row['text']
        clean_tweet = sen.clean_tweet(text_)
        sentiment = sen.get_tweet_sentiment(clean_tweet)
        sentiments.append([id_, text_, sentiment, dt_load])

    # for ln in data:
    #     clean_tweet = sen.clean_tweet(ln['text'])
    #     sentiment = sen.get_tweet_sentiment(clean_tweet)
    #     sentiments.append([ln['id'], ln['text'], sentiment, dt_load])
        

    df = pd.DataFrame(sentiments, columns=['id', 'text', 'sentiment', 'load_datetime'])


    with bigquery.get_client() as client:
        job = client.load_table_from_dataframe(
            dataframe=df,
            destination="SENTIMAX.sentiment_staging",
        )
        job.result()


# @graph
# def semx_graph():
#     stage_01 = st01_tweets_to_json()
#     stage_02 = st02_tweet_json_to_bq(stage_01)
#     stage_04 = st04_calc_sentiment()



