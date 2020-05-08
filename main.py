# Twitter Data Scraper written by Jack Chau (Tufts '22)

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
#from flatten_json import flatten #https://medium.com/@amirziai/flatten-json-on-python-package-index-pypi-9e4951693a5a
from pandas.io.json import json_normalize #https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
from contextlib import redirect_stdout

import pandas as pd
import json
import random
import time
import contextlib
import urllib3
import datetime

#from pandas.io.json import json_normalize #https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10

consumer_key = "_________insert_your_key_________";
consumer_secret = "_________insert_your_key_________";

access_token = "_________insert_your_key_________";
access_token_secret = "_________insert_your_key_________";

# Class for streaming and processing live tweets

class TwitterStreamer():
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = StdOutListener(fetched_tweets_filename)
        # Authentication process
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        stream = Stream(auth, listener)
        stream.filter(locations=coordinates_list, stall_warnings=True)

# Basic listener class

class StdOutListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            with open(self.fetched_tweets_filename, 'a', encoding='utf-8', newline='') as tf:
                new_time = datetime.datetime.now();
                new_date = new_time.strftime("%m-%d-%Y");
                new_name = new_date + ".csv"

                if (new_name != self.fetched_tweets_filename):
                    self.fetched_tweets_filename = new_name;

                json_format = json.loads(data) #return an object
                #NOTE TO SELF: geo_enabled is no longer supported: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

                if (json_format['coordinates']):
                    id_and_tweet = {
                        'user_id': json_format['user']['id'],
                        'user_tweet': json_format['text'],
                        'time': json_format['created_at'],
                        'lat': json_format['coordinates']['coordinates'][1],
                        'long': json_format['coordinates']['coordinates'][0]
                    }
                    json_df = json_normalize(id_and_tweet)
                    json_df.to_csv(tf, header=False, index=False, encoding='utf-8') #currently writing with header
                return True
        except BaseException as e:
            t = datetime.datetime.now();
            d = t.strftime("%m-%d-%Y %H:%M:%S");
            print("Error on data at %s: %s" % (d, str(e)))
        return True 

    def on_error(self, status):
        print("Error code 420. Stop code");
        if status == 420:
            return False

coordinates_list = [-180,-90,180,90];
datetime_object = datetime.datetime.now();
file_name = datetime_object.strftime("%m-%d-%Y");
fetched_tweets_filename = file_name + ".csv"
twitter_stream = TwitterStreamer();

while True:
    try:
        twitter_stream.stream_tweets(fetched_tweets_filename, coordinates_list);
    except urllib3.exceptions.ProtocolError:
        nsecs = random.randint(60,65)
        time.sleep(nsecs)
        continue
    except KeyboardInterrupt:
        break
    except:
        continue
