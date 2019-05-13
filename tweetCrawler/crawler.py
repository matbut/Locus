import twint
from .models import Tweet
import asyncio
from datetime import datetime


def crawl(crawl_parameters):

    # Configure
    c = twint.Config()
    c.Limit = 20
    c.Hide_output = False
    c.Store_object = True

    asyncio.set_event_loop(asyncio.new_event_loop())

    # Search
    if crawl_parameters.Content is not None:
        c.Search = crawl_parameters.Content
        twint.run.Search(c)

    tweets = twint.output.tweets_object
    print(len(tweets), 'tweets were downloaded.')

    # Save
    for tweet in tweets:
        print(dir(tweet))
        new_tweet = Tweet(
            content=tweet.tweet,
            date=datetime.utcfromtimestamp(tweet.datetime/1000.0).date(),
            time=datetime.utcfromtimestamp(tweet.datetime/1000.0).time(),
            username=tweet.username,
            link=tweet.link
        )
        new_tweet.save()
