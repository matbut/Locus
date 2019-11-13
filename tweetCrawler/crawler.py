import asyncio
import logging
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer

from search.models import SearchParameters
from .models import Tweet
from pathlib import Path
import twint
import json
import os

logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


class Crawler(SyncConsumer):
    def crawl(self, data):

        logging.info('Tweet crawler: starting')

        tweets_file_path = "output.json".format(str(Path.home()))
        search_id = data["parameters"]
        search_parameters = SearchParameters.objects.get(id=search_id)

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

        # Search
        if crawl_parameters.title is not None:
            c.Search = crawl_parameters.title
            twint.run.Search(c)
        '''

        # Search
        if search_parameters.url is not None:
            c.Search = search_parameters.url
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
                        id=tweet['id'],
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
                    new_tweet.searches.add(search_parameters)
            os.remove(tweets_file_path)

        # Send message
        sender_id = data["id"]
        async_to_sync(self.channel_layer.group_send)(
            sender_id,
            {
                'type': 'send_done',
                'message': 'tweet_crawler'
            }
        )
