import asyncio
import logging
import traceback
from datetime import datetime

import requests
import twint
from bs4 import BeautifulSoup
from channels.consumer import SyncConsumer
from django.db import transaction

from common import statusUpdate
from common.searcherUtils import send_to_worker, send_to_websocket, TWITTER_URL_SEARCHER_NAME, \
    TWITTER_TEXT_SEARCHER_NAME, WORKER_NAMES, add_parent, LINK_MANAGER_NAME, get_main_search, \
    search_cancelled
from common.url import clean_url
from search.models import Parent
from .models import Tweet, TwitterUser, Hashtag


def get_twint_configuration(tweets):
    c = twint.Config()
    c.Limit = 100
    c.Hide_output = True
    c.Popular_tweets = True
    c.Store_object = True
    c.Store_object_tweets_list = tweets
    return c


def add_hashtags(tweet, hashtags):
    for hashtag in hashtags:
        saved_hashtag, _ = Hashtag.objects.get_or_create(
            id=hashtag,
            link=f"https://twitter.com/hashtag/{hashtag}?src=hash"
        )
        tweet.hashtags.add(saved_hashtag)


def get_or_create(tweet, new_user):
    if Tweet.objects.filter(id=tweet.id).exists():
        return Tweet.objects.get(pk=tweet.id)
    else:
        epoch = int(tweet.datetime)
        result = Tweet(
            id=tweet.id,
            content=tweet.tweet,
            date=datetime.utcfromtimestamp(epoch / 1000.0).date(),
            time=datetime.utcfromtimestamp(epoch / 1000.0).time(),
            username=tweet.username,
            userlink=f"https://twitter.com/{tweet.username}",
            link=tweet.link,
            likes=tweet.likes_count,
            replies=tweet.replies_count,
            retweets=tweet.retweets_count,
            user=new_user,
        )
        result.save()
        add_hashtags(result, tweet.hashtags)
        return result


def get_avatar(user_id):
    c = twint.Config()
    c.User_id = user_id
    c.Hide_output = True
    c.Pandas = True
    twint.run.Lookup(c)
    users = twint.storage.panda.User_df
    avatar = users.get('avatar').tolist()[0] if 'avatar' in users.columns else ''
    twint.storage.panda.clean()
    return avatar

@transaction.atomic
def save_tweet(tweet, parent):
    user_avatar = get_avatar(tweet.user_id)

    new_user, _ = TwitterUser.objects.get_or_create(
        id=tweet.user_id,
        username=tweet.username,
        link=f"https://twitter.com/{tweet.username}",
        avatar=user_avatar,
    )

    new_tweet = get_or_create(tweet, new_user)
    add_parent(new_tweet, parent)
    return new_tweet.id, tweet.urls


class TwitterUrlSearcher(SyncConsumer):
    def __init__(self, scope):
        super().__init__(scope)
        self.name = TWITTER_URL_SEARCHER_NAME

    def log(self, level, message):
        logging.log(level, '[{0}] {1}'.format(self.name, message))

    def save_tweet(self, tweet, parent, where):
        try:
            save_tweet(tweet, parent)
            if where not in WORKER_NAMES:
                send_to_websocket(self.channel_layer, where=where, method='success', message='')
        except Exception as e:
            self.log(logging.WARNING, 'Object was not added to database: {}'.format(str(e)))

    def search_parameters_correct(self, msg):
        if not msg['body']['link']:
            self.log(logging.INFO, 'Link cannot be empty')
            return False
        return True

    def search(self, msg):

        self.log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())

        main_search_id = msg['body']['search_id']
        updater = statusUpdate.get(self.name)
        updater.in_progress(main_search_id)

        if search_cancelled(main_search_id):
            self.log(logging.INFO, 'Search cancelled, finishing')
            updater.success(main_search_id)
            return

        if not self.search_parameters_correct(msg):
            self.log(logging.INFO, 'Parameters incorrect, finishing')
            updater.success(main_search_id)
            return

        try:
            link = msg['body']['link']
            parent = Parent.from_dict(msg['body']['parent'])
            sender = msg['sender']

            # Configure
            tweets = []
            c = get_twint_configuration(tweets)

            # Search
            c.Search = link
            c.Links = "include"
            twint.run.Search(c)

            self.log(logging.INFO, f'{len(tweets)} tweets were downloaded.')

            for tweet in tweets:
                self.save_tweet(tweet, parent, sender)

            updater.success(main_search_id)
            self.log(logging.INFO, 'Finished')

        except Exception as e:
            print(traceback.format_exc())
            self.log(logging.ERROR, 'Failed: {0}'.format(str(e)))
            updater.failure(main_search_id)


def retrieve_html_title_and_description(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    description = soup.find('meta',  property='og:description')
    return soup.title.string if soup.title else None, description['content'] if description else None


class TwitterTextSearcher(SyncConsumer):
    def __init__(self, scope):
        super().__init__(scope)
        self.name = TWITTER_TEXT_SEARCHER_NAME

    def log(self, level, message):
        logging.log(level, '[{0}] {1}'.format(self.name, message))

    def save_tweet(self, tweet, parent, where):
        try:
            tweet_id, links = save_tweet(tweet, parent)
            if where not in WORKER_NAMES:
                send_to_websocket(self.channel_layer, where=where, method='success', message='')
            return tweet_id, links
        except Exception as e:
            self.log(logging.WARNING, 'Object was not added to database: {}'.format(str(e)))
            return None, None

    def search_parameters_correct(self, msg):
        if not msg['body']['title']:
            self.log(logging.INFO, 'Title cannot be empty')
            return False
        return True

    def search(self, msg):

        self.log(logging.INFO, 'Starting')
        asyncio.set_event_loop(asyncio.new_event_loop())

        main_search_id = msg['body']['search_id']
        updater = statusUpdate.get(self.name)
        updater.in_progress(main_search_id)

        if search_cancelled(main_search_id):
            self.log(logging.INFO, 'Search cancelled, finishing')
            updater.success(main_search_id)
            return

        if not self.search_parameters_correct(msg):
            self.log(logging.INFO, 'Parameters incorrect, finishing')
            updater.success(main_search_id)
            return

        try:
            main_search = get_main_search(main_search_id)
            title = msg['body']['title']
            parent = Parent.from_dict(msg['body']['parent'])
            sender = msg['sender']
            # Configure
            tweets=[]
            c = get_twint_configuration(tweets)

            # Search
            c.Search = title
            twint.run.Search(c)

            self.log(logging.INFO, f'{len(tweets)} tweets were downloaded.')

            for tweet in tweets:
                tweet_id, links = self.save_tweet(tweet, parent, sender)
                if tweet_id:
                    self.send_to_internet_search_manager(links, Parent(type=self.name, id=tweet_id), main_search.id)

            updater.success(main_search_id)

        except Exception as e:
            print(traceback.format_exc())
            self.log(logging.ERROR, 'Failed: {0}'.format(str(e)))
            updater.failure(main_search_id)

    def send_to_internet_search_manager(self, links, parent, search_id):
        for link in links:
            html_title, description = retrieve_html_title_and_description(link)
            statusUpdate.get(LINK_MANAGER_NAME).queued(search_id)
            send_to_worker(self.channel_layer, sender=self.name, where=LINK_MANAGER_NAME,
                           method='process_link', body={
                    'link': clean_url(link),
                    'parent': parent.to_dict(),
                    'search_id': search_id,
                    'title': html_title,
                    'snippet': description,
                })
