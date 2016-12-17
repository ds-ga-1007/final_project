"""
Date: 12/15/2016

Authors:Lingzhi Meng(lm3226)
        Yifu Sun(ys1700)
        Yanan Shi(ys2506)

Description: This file uses twitter API to collect tweets and save them as JSON files.
"""

#Import the necessary methods from tweepy library
import os, json, time,configparser, datetime,traceback
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = "701968263534788608-oa8MUBtcr09IphooUmELdSIcf1xM5wx"
access_token_secret = "v6Wch9hKdDXCYb9GbZQtIEYD9mZufqStOpXZSm0U2bK4V"
consumer_key = "oxZKuQ7yF9LTPYQqUqm0sRs03"
consumer_secret = "KrMKahnLAgSwgHyVEYeFMkMZNHIRaozMjn4i0W8uIy8GRlR32Y"

# File counter
path = "json/tweetJSON_"
counter = 0
file = None
tweetcounter = 0

# Listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):


    def on_data(self, data):
        global tweetcounter
        tweet = json.loads(data)
        location = tweet.get('coordinates')
        # Only store tweet with location data
        if(location != None):
            longitude = str('{:f}'.format(location['coordinates'][0]))
            latitude = str('{:f}'.format(location['coordinates'][1]))
            tweettext = tweet.get('text')
            tweetid = tweet.get('id_str')
            hashtag = tweet.get('entities').get('hashtags')
            tweetlang = tweet.get('lang')
            tweetplace = tweet.get('place')
            tweetcounter = tweetcounter + 1
            # Convert UTC time to ISO 8601 format
            timeString = tweet.get('created_at')
            timestampCS = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.strptime(timeString,'%a %b %d %H:%M:%S +0000 %Y'))
            timestampDB = time.strptime(timeString, '%a %b %d %H:%M:%S +0000 %Y')
            tweetJSON = parseJSON(latitude + ',' + longitude, timestampCS, tweettext, tweetid, hashtag, tweetlang, tweetplace)
            # Delete "[]" in the most outer layer
            storeFile(tweetJSON[1 : -1])
        return True

    def on_error(self, status):
        print (status)


# Parse tweet information into JSON format
def parseJSON(latlon, time, tweet, tweetid, hashtag, tweetlang, tweetplace):
    # JSON format required by CloudSearch, except outer "[]"
    tweetJSON = [
        {
            "type" : "add",
            "id" : tweetid,
            "fields" : {
                "coordinate" : latlon,
                "time" : time,
                "tweet" : tweet,
                "hashtag" : hashtag,
                "language" : tweetlang,
                "location" : tweetplace,
                "counts" : tweetcounter
            }
        }
    ]
    return json.dumps(tweetJSON)

def storeFile(data):
    global counter
    file.write(data)
    # Write comma to wait for next dictionary string
    file.write(",")
    # Max file size for AWS CloudSearch is 5MB
    if os.path.getsize(getCurrentFilename()) / 1024 / 1024 > 2:
        # Write right list quote if file exceeds certain size
        closeFile(file)
        counter = counter + 1
        openNewFile()

def openNewFile():
    global file, counter
    # Open the file that next to the last generated .json file
    while os.path.isfile(getCurrentFilename()):
        counter = counter + 1
    file = open(getCurrentFilename(), "a")
    # Write left "[" to start JSON format
    file.write("[")

def closeFile(file):
    file.close()
    with open(getCurrentFilename(), 'rb+') as f:
        f.seek(-1, 2)
        # Write right "]" to overwrite "," and close JSON format
        f.write(b']')
    f.close()

def getCurrentFilename():
    return path + str(counter) + ".json"

if __name__ == '__main__':
    while True:
        try:
            # Open file for appending
            openNewFile()
            # Handles Twitter authetification and the connection to Twitter Streaming API
            listener = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, listener)
            # Filter Twitter Streams to capture all tweets which enable geolocation
            stream.filter(locations = [-180, -90, 180, 90])
        except (KeyboardInterrupt, SystemExit):
            print("Quiting Getter...")
            break
        except Exception:
            traceback.print_exc()
        finally:
            closeFile(file)
    # Close database and file connection on exit
