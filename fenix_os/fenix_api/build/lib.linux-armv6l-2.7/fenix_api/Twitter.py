#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TwitterAPI import TwitterAPI

class Twitter:
    
    def __init__(self): # Constructor
        self.Main()

    def Main(self):
        consumer_key = 'jaL8cPgN86MiXI0tCLYEzC1xc'
        consumer_secret = 'okaIFI0m3dayTAk2w2qvjWJYjkNFkXxXzVzU9H9Pfmo47K5PZw'
        access_token_key = '4177870763-fOib4cgEjTbenGGAI4i3UeziszPiaUIrnSsiN4v'
        access_token_secret = 'h185EIXJY37Ex7LM5OR9dsrS9XLSV8ehrgRHZb67M5Hpp'
        api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
        r = api.request('search/tweets', {'q':'minitel'})
        print(r.status_code)
        for item in r:
            print(item)
    
