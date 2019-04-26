import twint
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from tweetCrawler.models import CrawlParameters

from .models import Tweet
import asyncio
from datetime import datetime

class Crawler(SyncConsumer):
    def crawl(self, data):

        sender_id = data["id"]

        crawl_parameters = CrawlParameters()
        crawl_parameters.Url = data["url"]

        # Configure
        c = twint.Config()
        c.Limit = 1
        c.Format = "Tweet id: {id} | Tweet: {tweet}"
        c.Hide_output = False
        c.Store_object = True

        asyncio.set_event_loop(asyncio.new_event_loop())

        # Search
        if crawl_parameters.Url is not None:
            c.Search = crawl_parameters.Url
            twint.run.Search(c)

        tweets = twint.output.tweets_object
        print(len(tweets), 'tweets were downloaded.')

        # Save
        for tweet in tweets:
            new_tweet = Tweet(
                content=tweet.tweet,
                date=datetime.utcfromtimestamp(tweet.datetime/1000.0).date(),
                time=datetime.utcfromtimestamp(tweet.datetime/1000.0).time(),
                username=tweet.username,
                link=tweet.link
            )
            new_tweet.save()


        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            sender_id,
            {
                'type': 'components',
                'message': 'done'
            }
        )