import time

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer


class Crawler(SyncConsumer):
    def process(self, data):
        #time.sleep(data)
        print("crawler: processing finished - ", data['duration'])
        async_to_sync(self.channel_layer.group_add)("testGroup", self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            "testGroup",
            {
                'type': "echo_msg",
                'msg': "sent from worker",
            })

    def echo_msg(self, message):
        print("Message to worker ", message)


class SomeComponent(SyncConsumer):
    def process(self, data):
        #time.sleep(data)
        print("crawler: processing finished - ", data['duration'])
        async_to_sync(self.channel_layer.group_add)("testGroup", self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            "testGroup",
            {
                'type': "echo_msg",
                'msg': "sent from worker",
            })

    def echo_msg(self, message):
        print("Message to worker ", message)


class AnotherComponent(SyncConsumer):
    def process(self, data):
        #time.sleep(data)
        print("crawler: processing finished - ", data['duration'])
        async_to_sync(self.channel_layer.group_add)("testGroup", self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            "testGroup",
            {
                'type': "echo_msg",
                'msg': "sent from worker",
            })

    def echo_msg(self, message):
        print("Message to worker ", message)
