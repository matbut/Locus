import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path

import twint
from channels.consumer import SyncConsumer

from common.searcherUtils import send_to_worker, send_to_websocket, TWITTER_URL_SEARCHER_NAME, \
    TWITTER_TEXT_SEARCHER_NAME, WORKER_NAMES, add_parent, INTERNET_SEARCH_MANAGER_NAME, get_main_search
from common import statusUpdate
from common.url import clean_url
from search.models import Parent
from .models import Tweet, TwitterUser


def get_twint_configuration(tweets_file_path):
    c = twint.Config()
    c.Limit = 100
    c.Hide_output = True
    c.Popular_tweets = True
    c.Store_json = True
    c.Output = tweets_file_path
    return c


def get_or_create(tweet, new_user):
    if Tweet.objects.filter(id=tweet['id']).exists():
        return Tweet.objects.get(pk=tweet['id'])
    else:
        epoch = int(tweet['created_at'])
        result = Tweet(
            id=tweet['id'],
            content=tweet['tweet'],
            date=datetime.utcfromtimestamp(epoch / 1000.0).date(),
            time=datetime.utcfromtimestamp(epoch / 1000.0).time(),
            username=tweet['username'],
            userlink=f"https://twitter.com/{tweet['username']}",
            link=tweet['link'],
            likes=tweet['likes_count'],
            replies=tweet['replies_count'],
            retweets=tweet['retweets_count'],
            user=new_user,
        )
        result.save()
        return result


def save_tweet(tweet_str, parent):
    tweet = json.loads(tweet_str)

    new_user, _ = TwitterUser.objects.get_or_create(
        id=tweet['user_id'],
        username=tweet['username'],
        link=f"https://twitter.com/{tweet['username']}",
    )

    new_tweet = get_or_create(tweet, new_user)
    add_parent(new_tweet, parent)
    return new_tweet.id, tweet['urls']


class TwitterUrlSearcher(SyncConsumer):
    def __init__(self, scope):
        super().__init__(scope)
        self.name = TWITTER_URL_SEARCHER_NAME

    def log(self, level, message):
        logging.log(level, '[{0}] {1}'.format(self.name, message))

    def save_tweet(self, tweet_str, parent, where):
        save_tweet(tweet_str, parent)
        if where not in WORKER_NAMES:
            send_to_websocket(self.channel_layer, where=where, method='success', message='')

    def search(self, msg):

        self.log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())

        updater = statusUpdate.get(self.name)
        updater.in_progress()

        try:
            tweets_file_path = '{0}/.locus/tmp_{1}.json'.format(str(Path.home()), self.name)

            link = msg['body']['link']
            parent = Parent.from_dict(msg['body']['parent'])
            sender = msg['sender']

            # Configure
            c = get_twint_configuration(tweets_file_path)

            # Search
            c.Search = link
            c.Links = "include"
            twint.run.Search(c)

            if os.path.isfile(tweets_file_path):
                with open(tweets_file_path, 'r') as tweets_file:
                    tweets = tweets_file.readlines()

                    self.log(logging.INFO, f'{len(tweets)} tweets were downloaded.')

                    for tweet_str in tweets:
                        self.save_tweet(tweet_str, parent, sender)

                os.remove(tweets_file_path)

            updater.success()
            self.log(logging.INFO, 'Finished')

        except Exception as e:
            self.log(logging.ERROR, 'Failed: {0}'.format(str(e)))
            updater.failure()


class TwitterTextSearcher(SyncConsumer):
    def __init__(self, scope):
        super().__init__(scope)
        self.name = TWITTER_TEXT_SEARCHER_NAME

    def log(self, level, message):
        logging.log(level, '[{0}] {1}'.format(self.name, message))

    def save_tweet(self, tweet_str, parent, where):
        tweet_id, links = save_tweet(tweet_str, parent)
        if where not in WORKER_NAMES:
            send_to_websocket(self.channel_layer, where=where, method='success', message='')
        return tweet_id, links

    def search(self, msg):

        self.log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())

        updater = statusUpdate.get(self.name)
        updater.in_progress()

        try:
            tweets_file_path = '{0}/.locus/tmp_{1}.json'.format(str(Path.home()), self.name)

            main_search = get_main_search(msg['body']['search_id'])
            title = msg['body']['title']
            parent = Parent.from_dict(msg['body']['parent'])
            sender = msg['sender']
            # Configure
            c = get_twint_configuration(tweets_file_path)

            # Search
            c.Search = title
            twint.run.Search(c)

            if os.path.isfile(tweets_file_path):
                with open(tweets_file_path, 'r') as tweets_file:
                    tweets = tweets_file.readlines()

                    self.log(logging.INFO, f'{len(tweets)} tweets were downloaded.')

                    for tweet_str in tweets:
                        tweet_id, links = self.save_tweet(tweet_str, parent, sender)
                        self.send_to_internet_search_manager(links, Parent(type=self.name, id=tweet_id), main_search.id)

                os.remove(tweets_file_path)

            updater.success()

        except Exception as e:
            self.log(logging.ERROR, 'Failed: {0}'.format(str(e)))
            updater.failure()

    def send_to_internet_search_manager(self, links, parent, search_id):
        for link in links:
            statusUpdate.get(INTERNET_SEARCH_MANAGER_NAME).queued()
            send_to_worker(self.channel_layer, sender=self.name, where=INTERNET_SEARCH_MANAGER_NAME,
                           method='process_link', body={
                    'link': clean_url(link),
                    'parent': parent.to_dict(),
                    'search_id': search_id
                })
