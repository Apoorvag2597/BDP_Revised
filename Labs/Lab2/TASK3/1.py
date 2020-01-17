import sys
import json
import time
import tweepy
import socket


CONSUMER_KEY = 'y37L6Vykcr0AvxvDf10axhKsc'
CONSUMER_SECRET = 'K8Sk4VSDTp0ijSgqBQ5tk8eAXfa1gcQbNoGkm8a3KKzDTdz2a9'
ACCESS_TOKEN = '2886203293-rx1AypFuSuAmNrjLeFI0ShrwpUbz8R2SZuRDU0H'
ACCESS_TOKEN_SECRET ='qKpWIQ7ujh8aA1eHlVzyrGcptWqjXZh9rUaTxn0T5yN7x'

def validTweet(str_tweet):
    json_tweet = json.loads(str_tweet)
    return False if list(json_tweet.keys())[0] == 'delete' or list(json_tweet.keys())[0] == 'limit' else True

class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self, csocket):
        self.client_socket = csocket

    def on_data(self, data):
        if validTweet(data):
            tweet = json.loads(data)
            self.client_socket.send(tweet["text"].encode('utf-8'))

    def on_error(self, status):
        print(status)

def main():
    global CONSUMER_KEY
    global CONSUMER_SECRET
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET

    # Create socket
    s = socket.socket()
    host = 'localhost'
    port = 9000
    s.bind((host, port))
    s.listen(3)
    c_scoket, addr = s.accept()
    time.sleep(3)

    # Twitter streaming
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = tweepy.Stream(auth, TwitterStreamListener(c_scoket))
    stream.filter(languages=['en'], track=['bofa','usbank','discover'])

if __name__ == '__main__':
    main()