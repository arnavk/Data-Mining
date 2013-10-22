from tweepy import StreamListener
import json, time, sys, os

class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dest_dir = os.path.join(script_dir, 'streaming_data_lang')
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass # already exists
        path = os.path.join(dest_dir, fprefix + '.' 
                            + time.strftime('%Y%m%d-%H%M%S') + '.json')

        self.output  = open(path, 'w')
        self.delout  = open('delete.txt', 'a')

    def on_data(self, data):

        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return false

    def clean (self, tweet):
        created_at = tweet['created_at']
        id_str = tweet['id_str']
        text = tweet['text']
        user_id = tweet['user']['id_str']
        user_handle = tweet['user']['screen_name']
        hashtags_raw = tweet['entities']['hashtags']
        hashtags = list()
        for x in range(0, len(hashtags_raw)):
            hashtags.append(hashtags_raw[x]['text'])
        if tweet['geo'] != None:
            coord = tweet['coordinates']['coordinates']
            coord.reverse()
        else:
            coord_raw = tweet['place']['bounding_box']['coordinates']
            x1y1 = coord_raw[0][0]
            x3y3 = coord_raw[0][2]
            xx = (x3y3[0] + x1y1[0])/2
            yy = (x3y3[1] + x1y1[1])/2
            coord = [yy,xx]
        if tweet['place'] != None:
            country = tweet['place']['country']
            country_code = tweet['place']['country_code']
        else:
            country = "Unknown"
            country_code = "UNKN"
        lang = tweet['lang']
        clean_tweet = {}
        clean_tweet['created_at'] = created_at
        clean_tweet['id_str'] = id_str
        clean_tweet['text'] = text
        clean_tweet['user_id'] = user_id
        clean_tweet['user_handle'] = user_handle
        clean_tweet['hashtags'] = hashtags
        clean_tweet['coord'] = coord
        clean_tweet['country_code'] = country_code
        clean_tweet['country'] = country
        clean_tweet['lang'] = lang

        return json.dumps(clean_tweet)
        
    def on_status(self, status):

        tweet = json.loads(status)
        if tweet['lang'] != 'en':
            return

        clean_tweet = self.clean(tweet)    
        self.output.write(clean_tweet + "\n")

        self.counter += 1

        if self.counter >= 10000:
            self.output.close()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            dest_dir = os.path.join(script_dir, 'streaming_data_lang')
            try:
                os.makedirs(dest_dir)
            except OSError:
                pass # already exists
            path = os.path.join(dest_dir, self.fprefix + '.' 
                               + time.strftime('%Y%m%d-%H%M%S') + '.json')
            self.output = open(path, 'w')
            self.counter = 0

        return

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(str(track) + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 