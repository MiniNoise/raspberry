#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TwitterAPI import TwitterAPI
import time

class FenixTwitter:

    media_url = []
    
    def __init__(self): # Constructor
        self.Main()

    def Main(self):
        consumer_key = 'ZRgXWodHhxDvySQ6hrp9K5LKm'
        consumer_secret = 'y8Tj7mx3LKsmnoUom5niJKWD4OOk5x7Up5XUUDj1kUjZsoibFx'
        access_token_key = '841412456769552386-Dcqma3HyLMo0JYRHO82yP6kl5Q5Yknb'
        access_token_secret = 'OVnwSaKlpLizTp4e3KOfnpCrb93Df7enh2sosGDfJa3q9'
        self.api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    
    def Request(self):
        r = self.api.request('statuses/home_timeline', {'count':1})
        return r

    def SendTweet(self, tweet):
        r = self.api.request('statuses/update', {'status':tweet})
        return r

    def GetMediaList(self):
        return self.media_url

    def GetTweets(self):
        r = ''
        try:
            r = self.api.request('search/tweets', {'q':'#ShowHello', 'count':'200'})
        except Exception as e:
           time.sleep(1)
           print("failed")
           self.GetTweets()
        tweets = []
        self.media_url[:] = []
        for item in r:
            item['text'].encode("utf-8", errors='ignore')
            item['text'] = item['text'].replace('\n', '. ')
            if item['text'][0:2] != 'RT':
                try:
                    for media in item['entities']['media']:                    
                        self.media_url.append(media['media_url'])
                except KeyError as e:
                    e = e
                
                tweets.append(item['text'])
        return tweets
        
