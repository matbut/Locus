from channels.routing import ProtocolTypeRouter, ChannelNameRouter
from crawler.crawler import Crawler
from crawler.crawler import SomeComponent
from crawler.crawler import AnotherComponent

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        'crawler': Crawler,
        'some_component': SomeComponent,
        'another_component': AnotherComponent,
    })
})
