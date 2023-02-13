import json
import os
import requests
import pulsar
import logging
import time
from collections import defaultdict
import tweepy
from pulsar.schema import *
import pandas as pd
import datetime

#########################################
Record = pulsar.schema.Record
Integer = pulsar.schema.Integer
String = pulsar.schema.String


bearer_token = os.environ.get("BEARER_TOKEN")
twitter_client = tweepy.Client(bearer_token)
params = {"expansions": 'author_id,referenced_tweets.id',
          "tweet.fields": "entities"}


class Example(Record):
    Tweet = String()
    following = Integer()
    followers = Integer()
    actions = Integer()
    is_retweet = Integer()
    location = String()
    created_at = String()
    tweet_id = String()


# edit area here
filter_rules = [{"value": 'abortion lang:en'}]

# edit area end


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(
                response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )


def set_rules(delete):
    # adjust the rules if needed

    payload = {"add": filter_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(
                response.status_code, response.text)
        )
    logging.info(json.dumps(response.json()))
    print(response)


def get_stream():
    producer = Producer()

    df = pd.read_csv('data/test/tweets.csv')
    for row in df.iterrows():
        row_json = row[1].to_json()
        producer.produce_messages(row_json)


class Producer(object):
    """
    Create a pulsar producer that writes random messages to a topic
    """

    def __init__(self):
        self.token = os.getenv("ASTRA_STREAMING_TOKEN")
        self.service_url = os.getenv("ASTRA_STREAMING_URL")
        self.topic = os.getenv("ASTRA_TOPIC")
        self.client = pulsar.Client(self.service_url,
                                    authentication=pulsar.AuthenticationToken(self.token))
        self.producer = self.client.create_producer(topic=self.topic)
        self.bearer_token = os.getenv("BEARER_TOKEN")

    def produce_messages(self, s):
        """
        Create and send random messages
        """
        self.producer.send(s.encode('utf-8'))
        logging.info("Just wrote: {}".format(s))
        print("Just wrote: {}".format(s))
        time.sleep(5)


def main():
    # rules = get_rules()
    # delete = delete_all_rules(rules)
    # set = set_rules(delete)
    get_stream()


if __name__ == "__main__":
    main()
