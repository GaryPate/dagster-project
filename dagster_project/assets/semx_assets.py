import tweepy
import json
import re
from datetime import datetime, timedelta
import pandas as pd
from dagster_gcp import BigQueryResource
from textblob import TextBlob
from dagster import asset
from typing import List


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



@asset(compute_kind="python", group_name="sentimax_compute")
def st01_tweets_to_json() -> None:
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

    # return_ls = []
    # for tweet in tweets_data:
    #     return_ls.append({'id': tweet.id, 'text': tweet.text})

    # return return_ls
    with open('/data/tweet_data.json', 'w') as f:
        for tweet in tweets_data:
            print(tweet)
            f.write(json.dumps({'id': tweet.id, 'text': tweet.text}) + "\n")


@asset(compute_kind="python", group_name="sentimax_compute", deps=[st01_tweets_to_json])
def st02_tweet_json_to_bq(bigquery: BigQueryResource) -> None:
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
            destination="SENTIMAX.st02_tweet_json_to_bq",   #tweet_data_staging",
        )
        job.result()



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

# @multi_asset(
#     outs={
#         name: AssetOut(key=asset_key)
#         for name, asset_key in get_asset_keys_by_output_name_for_source(
#             [dagster_dbt_assets], "SENTIMAX"
#         ).items()
#     }
# )
# def multi_dbt_asset(context):
#     output_names = list(context.selected_output_names)
#     yield Output(value=..., output_name=output_names[0])
#     #yield Output(value=..., output_name=output_names[1])


@asset(
    compute_kind="python", group_name="sentimax_compute",
    # deps=[st02_tweet_json_to_bq],
    #deps=[st02_tweet_json_to_bq], #list(multi_dbt_asset)[0], #get_asset_key_for_source([dagster_dbt_assets], "stg03_tweet_increment"),
    #ins={"st02_tweet_json_to_bq": AssetIn("st02_tweet_json_to_bq")}
)
def st03_calc_sentiment(st02_tweet_json_to_bq: pd.DataFrame, bigquery: BigQueryResource) -> None:   #  , tweet_history: pd.DataFrame
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

    for index, row in st02_tweet_json_to_bq.iterrows():
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
            destination="SENTIMAX.st03_calc_sentiment",
        )
        job.result()


# @graph
# def semx_graph():
#     stage_01 = st01_tweets_to_json()
#     stage_02 = st02_tweet_json_to_bq(stage_01)
#     stage_04 = st04_calc_sentiment()



