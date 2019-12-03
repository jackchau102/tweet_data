from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from flatten_json import flatten #https://medium.com/@amirziai/flatten-json-on-python-package-index-pypi-9e4951693a5a
from pandas.io.json import json_normalize #https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10

import pandas as pd
import json



def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


# def pick_and_flatten(key):
#     if key == "user":
#         to_flatten = json.loads(key)
#         flatten(to_flatten)

# Class for streaming and processing live tweets

class TwitterStreamer():
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = StdOutListener(fetched_tweets_filename)
        # Authentication process
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        stream = Stream(auth, listener) 
        # stream.filter(locations=coordinates_list)
        stream.filter(track="New York City")

# Basic listener class

class StdOutListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try: 
            # user_info = [];
            with open(self.fetched_tweets_filename, 'a') as tf:
                # tf.write(data);
                # print(data)
                json_format = json.loads(data) #return an object
                #NOTE TO SELF: geo_enabled is no longer supported: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

                if (json_format['user'] == False):
                    print("False")
                elif (json_format['user']):
                    print("True")
                    id_and_tweet = {
                        'user_id': json_format['user']['id'],
                        'user_tweet': json_format['text'],
                        'user_location': json_format['user']['location']
                    }
                    json_df = json_normalize(id_and_tweet)
                    json_df.to_csv(tf, header=False, encoding='utf-8') #currently writing with header
                return True
        except BaseException as e:
            with open('error.json', 'a') as tf:
                tf.write(data)
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            return False

# class JSONparse():
#     def print_stuff()

coordinates_list = [47.419126, -124.378023, 27.002140, -78.886330];
fetched_tweets_filename = "out.csv"

twitter_stream = TwitterStreamer()
twitter_stream.stream_tweets(fetched_tweets_filename, coordinates_list)
