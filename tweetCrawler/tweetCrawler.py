import twint
from .models import Tweet


def crawl(crawl_parameters):

    # Configure
    c = twint.Config()
    c.Limit = 20
    c.Format = "Tweet id: {id} | Tweet: {tweet}"
    c.Hide_output = False
    c.Store_object = True

    # Search
    if crawl_parameters.Content is not None:
        c.Search = crawl_parameters.Content
        twint.run.Search(c)
    if crawl_parameters.Url is not None:
        c.Search = crawl_parameters.Url
        twint.run.Search(c)
    if crawl_parameters.Title is not None:
        c.Search = crawl_parameters.Title
        twint.run.Search(c)

    tweets = twint.output.tweets_object
    print(len(tweets), 'tweets were downloaded.')

    # Save
    for tweet in tweets:
        print(dir(tweet))
        new_tweet = Tweet(
            content=tweet.tweet,
            date=tweet.date,
            time=tweet.time,
            username=tweet.username,
            link=tweet.link
        )
        new_tweet.save()
