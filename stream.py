from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from secrets import atoken, asecret, ckey, csecret
import json

stored_tweets = []  # ugly global variable which is used in Listener

class Listener(StreamListener):
    def __init__(self, volume_):
        self.volume_ = volume_  # volume (number) of tweets to record
    
    def on_data(self, data):  # use on status instead of on data??? 
        json_data = json.loads(data)
        tweet_text = json_data["text"]
        # get tweet of extended size
        if "extended_tweet" in json_data:
            tweet_text = json_data['extended_tweet']['full_text']
        if "retweeted_status" in json_data and 'extended_tweet' in json_data['retweeted_status']:
            tweet_text = json_data['retweeted_status']['extended_tweet']['full_text']
            
        tweet_username = json_data["user"]["screen_name"]
        tweet_id = json_data["id"]
        #write json to file
        stored_tweets.append({
            'tweet_id' : tweet_id,
            'tweet_username' : tweet_username,
            'tweet_text' : tweet_text
        })
        if self.volume_ <= 1:
            return False  # close the listener when volume met (NOT WORKING)
        else:
            self.volume_ = self.volume_ - 1

    def on_error(self, status):
        print(status)

def replace_str_index(text,index,replacement):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])
    
'''generates a list of entered string with astrisks substited all possible ways'''
def gen_substitutions(string):
    substitutions_set = set()
    for i in range(len(string)):
        if string[i] == '*':
            continue
        substitution = replace_str_index(string, i, '*')
        substitutions_set.add(substitution)
        sub_subs = gen_substitutions(substitution)
        substitutions_set |= sub_subs
    return substitutions_set

'''
Get the subset of in set that consists of elements containing n astrisk characters.
Parameters:
s (set): set to filter
n (int): number of astrisks desired in each element of returned subset
'''
def filter_n_subs(s, n):
    subset = set()
    for string in s:
        asterisk_count = 0
        for char in string:
            if char ==  '*':
                asterisk_count += 1
        if asterisk_count == n:
            subset.add(string)
    return subset   

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
base_word = input("Keyword:")
num_subs = int(input("Subs:"))
vol = 250
#vol = int(input("Volume of tweets:"))

#handle edge case of zero subs 
if num_subs == 0:
    filter_list = [base_word]
else:
    filter_words = filter_n_subs(gen_substitutions(base_word), num_subs)
    filter_list = list(filter_words)
print(filter_list)

try:
    twitterStream = Stream(auth, Listener(volume_=vol), tweet_mode= "extended")
    twitterStream.filter(track=filter_list)    
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stored_tweets = {tweet['tweet_id']:tweet for tweet in stored_tweets}.values()  # remove duplicates from list 
    with open('../data/'+str(base_word)+str(num_subs)+'.json', 'w') as outfile:
                json.dump(list(stored_tweets), outfile, indent=2)
    twitterStream.disconnect()
