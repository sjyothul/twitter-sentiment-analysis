import tweepy
import csv
import re
import datetime
from nltk.corpus import stopwords
import numpy as np
from nltk import sent_tokenize, word_tokenize as word_tokenize,pos_tag
from textblob import TextBlob
from nltk.stem import PorterStemmer
import pandas as pd
from nltk.tokenize import word_tokenize

ps=PorterStemmer()

consumer_key = "xb5jiZO0C3IYXjSvo6NT9hs9c"
consumer_secret = "5bcBOFElxcfXB2Miw5T3gv1IDdjbgh9Zdvd8PI9Q3oyUCWkBRZ"
access_key = "4818331753-j8cXBXV1dedQoZa1QyMOo6F5MCrWV0fwJixxKmZ"
access_secret = "wikjVtbCXSEHVO5eZFoV1ipQfzxOS8jBcAWbSe2BEwkFE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth) 

stop_words = set(stopwords.words('english'))
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
csvFile = open('final5.csv', 'a')
csvWriter = csv.writer(csvFile)
reg_result=''
dictionary={}

csvWriter.writerow(['user_name','date:time','tweet','reply_count','retweet_count','tagged','polarity'])
for full_tweets in tweepy.Cursor(api.search,q="happy",lang="en",since="2018-06-17",tweet_mode="extended").items():
    count=0
    for tweet in tweepy.Cursor(api.search,q='to:'+full_tweets.user.screen_name).items():
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
              count=count+1
    #print count
    #print full_tweets.retweet_count
    clean= re.sub(r"http\S+", "", full_tweets.full_text)
    clean1= re.sub(r"RT ", "", clean)
	#print (tweet.user.screen_name,tweet.created_at,clean1)
    pattern=emoji_pattern.sub(r'',clean1.encode('utf-8'))
	#print (tweet.user.screen_name,tweet.created_at,pattern)
    row=re.sub( '[^a-zA-Z0-9_\- ]+','',str(pattern))
    reg_result+=row
    sentence=reg_result
    word_tokens=word_tokenize(reg_result.lower())
    filtered_sentence=[w for w in word_tokens if not w in stop_words]
    tagged=pos_tag(filtered_sentence)
    for w in filtered_sentence:
           blob = TextBlob(w).sentiment
           dictionary[w]=blob
           print (w,blob)
    print "\n---------------------------------------\n"
    #print (full_tweets.user.screen_name,full_tweets.created_at,sentence,count,full_tweets.retweet_count,tagged,dictionary)
    csvWriter.writerow([full_tweets.user.screen_name,full_tweets.created_at,sentence,count,full_tweets.retweet_count,tagged,dictionary])
    dictionary={}
    reg_result=''

df = pd.read_csv('final5.csv')
cd=df.user_name.nunique()
print "no of unique users is :"
print(cd)
gh=df.drop_duplicates().user_name.value_counts()
print(gh)
df = pd.read_csv('final5.csv')
df.reset_index().set_index(['user_name']).sortlevel(0).to_csv('finals.csv')













