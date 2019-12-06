from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from flatten_json import flatten #https://medium.com/@amirziai/flatten-json-on-python-package-index-pypi-9e4951693a5a
from pandas.io.json import json_normalize #https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10

import pandas as pd
import json
import random

consumer_key = "JStINnJylOAKUs1hxGQB4IjmH";
consumer_secret = "K0LBbNpkrO2fYzG2domSs3k6nCiSyPZDhCepTB9CHCjlpHY944";

access_token = "1196832929525055488-G7nOefU8MkLVSMDNWw72sVeZNq1YDg";
access_token_secret = "Qi8BM3NHGIslYoawrnYbq0U5fMbm7RVcbMcklU7VsZU8p";

# def flatten_json(y):
#     out = {}

#     def flatten(x, name=''):
#         if type(x) is dict:
#             for a in x:
#                 flatten(x[a], name + a + '_')
#         elif type(x) is list:
#             i = 0
#             for a in x:
#                 flatten(a, name + str(i) + '_')
#                 i += 1
#         else:
#             out[name[:-1]] = x

#     flatten(y)
#     return out


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
        stream.filter(locations=coordinates_list)
        # stream.filter(track="New York City")

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

                # if (json_format['user'] == False):
                #     print("False")
                if (json_format['coordinates']):
                #     print("True")
                    id_and_tweet = {
                        'user_id': json_format['user']['id'],
                        'user_tweet': json_format['text'],
                        'coordinates': json_format['coordinates']['coordinates']
                    }
                    json_df = json_normalize(id_and_tweet)
                    json_df.to_csv(tf, header=False, index=False, encoding='utf-8') #currently writing with header
                return True
        except BaseException as e:
            nsecs=random.randint(60,63)
            time.sleep(nsecs)
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            return False

coordinates_list = [-124.763,24.5231,-66.9499,49.3844];
fetched_tweets_filename = "out.csv"

twitter_stream = TwitterStreamer()
twitter_stream.stream_tweets(fetched_tweets_filename, coordinates_list)

# # Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# # MySQLdb module written by Andy Dustman, documentation at http://mysql-python.sourceforge.net/MySQLdb.html
# # GeoSearch crawler written by Chris Cantey, MS GIS/Cartography, University of Wisconsin, https://geo-odyssey.com
# # MwSQLdb schema written with great assistance from Steve Hemmy, UW-Madison DoIT


# from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
# from tweepy import Stream
# import time
# import MySQLdb
# import csv
# import random

# # Go to http://dev.twitter.com and create an app. 
# # The consumer key and secret as well as the access_token and secret will be generated for you after you register with Twitter Developers

# # consumer_key = "Pwb3M4k13Gr2QAXaIHGG3HwQn"
# # consumer_secret = "NP2vjVYdfHrVffQglhWz4LzgxWpP0rrY8aUNprecpBSo5Ohshg"
# # access_token = "50997367-eCfcVqU5A4VfszFtXFwGKukeINuo33xS0CbtQPeiD"
# # access_token_secret = "6OxF6a6zVtvDUtV00bM3KgAufl3ycTSD38UIergji4YkZ"

# consumer_key = "JStINnJylOAKUs1hxGQB4IjmH";
# consumer_secret = "K0LBbNpkrO2fYzG2domSs3k6nCiSyPZDhCepTB9CHCjlpHY944";

# access_token = "1196832929525055488-G7nOefU8MkLVSMDNWw72sVeZNq1YDg";
# access_token_secret = "Qi8BM3NHGIslYoawrnYbq0U5fMbm7RVcbMcklU7VsZU8p";


# Coords = dict()
# XY = []

# # per request, write output to csv, rather than mysql. Be aware of limited rows to csv. The streaming API will return millions of rows per day.
# csvfile = open('geopy_results.csv','wb')
# csvwriter = csv.writer(csvfile)
# csvwriter.writerow(['UserID', 'Date', 'Lat', 'Long', 'Text'])

# class StdOutListener(StreamListener):
#     """ A listener handles tweets that are the received from the stream.
#     This is a basic listener that inserts tweets into MySQLdb.
#     """
#     def on_status(self, status):
#         # print "Tweet Text: ",status.text
#         text = status.text
#         # print "Time Stamp: ",status.created_at
#         try:
#             Coords.update(status.coordinates)
#             XY = (Coords.get('coordinates'))  #Place the coordinates values into a list 'XY'
#             # print "X: ", XY[0]
#             # print "Y: ", XY[1]
#         except:
#             # Often times users opt into 'place' which is neighborhood size polygon
#             # Calculate center of polygon
#             Box = status.place.bounding_box.coordinates[0]
#             XY = [(Box[0][0] + Box[2][0])/2, (Box[0][1] + Box[2][1])/2]
#             # print "X: ", XY[0]
#             # print "Y: ", XY[1]
#             pass
#         # Comment out next 4 lines to avoid MySQLdb to simply read stream at console
#         # row = [status.id_str, str(status.created_at), str(XY[1]), str(XY[0]), text]
#         # csvwriter.writerow(row)
                                
#         # Alternatively write to CSV. CSV's. limited
#         csvwriter.writerow([unicode(status.id_str).encode("utf-8"),unicode(status.created_at).encode("utf-8"),XY[1],XY[0],unicode(status.text).encode("utf-8")])
                      

# def main():
#     l = StdOutListener()    
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     stream = Stream(auth, l, timeout=30.0)
#     # Only records 'locations' OR 'tracks', NOT 'tracks (keywords) with locations'
#     while True:
#         try:
#             # Call tweepy's userstream method 
#             # Use either locations or track, not both
#             stream.filter(locations=[-124.763,24.5231,-66.9499,49.3844], async=False)##These coordinates are approximate bounding box around USA
#             # stream.filter(track=['obama'])## This will feed the stream all mentions of 'keyword'
#             break
#         except Exception, e:
#              # Abnormal exit: Reconnect
#              nsecs=random.randint(60,63)
#              time.sleep(nsecs)            

# if __name__ == '__main__':
#     main()