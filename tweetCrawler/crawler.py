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

        crawl_parameters = CrawlParameters(data["parameters"])

        # Configure
        c = twint.Config()
        c.Limit = 20
        c.Hide_output = False
        c.Store_object = True

        asyncio.set_event_loop(asyncio.new_event_loop())


        # Search
        if crawl_parameters.url is not None:
            c.Search = crawl_parameters.url
            twint.run.Search(c)

        tweets = twint.output.tweets_object
        print(len(tweets), 'tweets were downloaded.')

        # Save
        for tweet in tweets:
            new_tweet = Tweet(
                content=tweet.tweet,
                date=datetime.utcfromtimestamp(tweet.datetime / 1000.0).date(),
                time=datetime.utcfromtimestamp(tweet.datetime / 1000.0).time(),
                username=tweet.username,
                link=tweet.link
            )
            new_tweet.save()

        # Send message
        async_to_sync(self.channel_layer.group_send)(
            sender_id,
            {
                'type': 'send_done',
                'message': 'tweet_crawler'
            }
        )
