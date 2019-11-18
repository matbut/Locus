import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path

import twint
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer

from googleCrawlerOfficial.models import GoogleResultOfficial
from search.models import CrawlParameters, SearchParameters
from .models import Tweet

logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


class Crawler(SyncConsumer):
    def crawl(self, data):

        logging.info('Tweet crawler: starting')

        tweets_file_path = "output.json".format(str(Path.home()))

        crawl_parameters = CrawlParameters.from_dict(data["parameters"])

        search_id = data.get("search_id")
        search_parameters = None
        if search_id is not None:
            search_parameters = SearchParameters.objects.get(id=search_id)

        google_id = data.get("google_id")
        google = None
        if google_id is not None:
            google = GoogleResultOfficial.objects.get(id=google_id)

        # Configure
        c = twint.Config()
        c.Limit = 100
        c.Hide_output = True
        #c.Store_object = True
        c.Store_json = True
        c.Output = tweets_file_path

        asyncio.set_event_loop(asyncio.new_event_loop())

        '''
        # Search
        if crawl_parameters.content is not None:
            c.Search = crawl_parameters.url
            twint.run.Search(c)
        '''

        # Search
        if crawl_parameters.title != "":
            c.Search = crawl_parameters.title
            twint.run.Search(c)

        # Search
        if crawl_parameters.url != "":
            c.Search = crawl_parameters.url
            twint.run.Search(c)

        if os.path.isfile(tweets_file_path):
            with open(tweets_file_path, "r") as tweets_file:
                tweets = tweets_file.readlines()

                logging.info(f'{len(tweets)} tweets were downloaded.')

                # Save
                for tweet_str in tweets:
                    tweet = json.loads(tweet_str)
                    epoch = int(tweet['created_at'])
                    new_tweet = Tweet(
                        tweet_id=tweet['id'],
                        content=tweet['tweet'],
                        date=datetime.utcfromtimestamp(epoch / 1000.0).date(),
                        time=datetime.utcfromtimestamp(epoch / 1000.0).time(),
                        username=tweet['username'],
                        userlink= f"https://twitter.com/{tweet['username']}",
                        link=tweet['link'],
                        likes=tweet['likes_count'],
                        replies=tweet['replies_count'],
                        retweets=tweet['retweets_count']
                    )
                    new_tweet.save()
                    if search_id is not None:
                        new_tweet.searches.add(search_parameters)
                    if google_id is not None:
                        new_tweet.google.add(google)
            os.remove(tweets_file_path)

        # Send message
        sender_id = data["id"]
        if sender_id == "google_crawler":
            async_to_sync(self.channel_layer.send)(
                sender_id,
                {
                    'type': 'send_done',
                    'message': 'tweet_crawler'
                }
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                sender_id,
                {
                    'type': 'send_done',
                    'message': 'tweet_crawler'
                }
            )
