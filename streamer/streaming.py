from slistener import SListener
import time, tweepy, sys

consumer_key ="WR6mdm3TF2xfJIHriOHIQ"
consumer_secret = "iDXasX2YAuFEeA3PidKmMISSwEv4fPrCZXeX3uwo"
access_token = "483024889-diwBaFCMcRHD7o3sfqYJhsfGKv1F9Q1lFje6vi7E"
access_token_secret = "hFBu2KUmZdn4gglbflFbYMv56mmCA2KfmCunbnyaCNo"

# OAuth process, using the keys and tokens

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def main():
    track = ['obama', 'romney']
 
    listen = SListener(api, 'streamer')
    stream = tweepy.Stream(auth, listen)
    boundingBox = [-180,-90,180,90]
    print "Streaming started..."

    # try: 
    stream.filter(locations = boundingBox)
    # except:
    #     print "error!"
    #     stream.disconnect()

if __name__ == '__main__':
    main()