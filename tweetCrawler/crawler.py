import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path

import twint
from channels.consumer import SyncConsumer

from common.crawlerUtils import retrieve_params, send_message, group_send_message
from googleCrawlerOfficial.models import GoogleResultOfficial
from .models import Tweet

component = 'twitter'


def log(level, message):
    logging.log(level, '[twitter] {0}'.format(message))


def get_twint_configuration(tweets_file_path):
    c = twint.Config()
    c.Limit = 100
    c.Hide_output = True
    c.Popular_tweets = True
    c.Store_json = True
    c.Output = tweets_file_path
    return c


def save_tweet(tweet_str, search_parameters, google):
    tweet = json.loads(tweet_str)
    epoch = int(tweet['created_at'])
    new_tweet = Tweet(
        id=tweet['id'],
        content=tweet['tweet'],
        date=datetime.utcfromtimestamp(epoch / 1000.0).date(),
        time=datetime.utcfromtimestamp(epoch / 1000.0).time(),
        username=tweet['username'],
        userlink=f"https://twitter.com/{tweet['username']}",
        link=tweet['link'],
        likes=tweet['likes_count'],
        replies=tweet['replies_count'],
        retweets=tweet['retweets_count']
    )
    new_tweet.save()
    if search_parameters is not None:
        new_tweet.searches.add(search_parameters)
    if google is not None:
        new_tweet.google.add(google)


class Crawler(SyncConsumer):
    def crawl(self, data):

        log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())
        sender_id = data['id']

        try:
            tweets_file_path = 'output.json'.format(str(Path.home()))

            search_parameters, crawl_parameters = retrieve_params(data)

            google_id = data.get('google_id')
            google = GoogleResultOfficial.objects.get(link=google_id) if google_id is not None else None

            # Configure
            c = get_twint_configuration(tweets_file_path)

            # Search
            if crawl_parameters.title != '':
                c.Search = crawl_parameters.title
                twint.run.Search(c)

            # Search
            if crawl_parameters.url != '':
                c.Search = crawl_parameters.url
                c.Links = "include"
                twint.run.Search(c)

            if os.path.isfile(tweets_file_path):
                with open(tweets_file_path, 'r') as tweets_file:
                    tweets = tweets_file.readlines()

                    log(logging.INFO, f'{len(tweets)} tweets were downloaded.')

                    for tweet_str in tweets:
                        save_tweet(tweet_str, search_parameters, google)

                os.remove(tweets_file_path)

            # Send message
            if sender_id == 'google_crawler':
                send_message(component, self.channel_layer, sender_id,
                             {'type': 'send_done', 'message': 'tweet_crawler'})
            else:
                group_send_message(component, self.channel_layer, sender_id, 'send_done', 'tweet_crawler')

        except Exception as e:
            log(logging.ERROR, str(e))
            message = 'tweet_crawler: {0}'.format(str(e))
            if sender_id == 'google_crawler':
                send_message(component, self.channel_layer, sender_id, {'type': 'send_failure', 'message': message})
            else:
                group_send_message(component, self.channel_layer, sender_id, 'send_failure', message)
