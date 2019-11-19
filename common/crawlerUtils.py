import logging

from asgiref.sync import async_to_sync

from search.models import SearchParameters, CrawlParameters

logging.basicConfig(format='[%(asctime)s] %(message)s')
logging.getLogger().setLevel(logging.INFO)


def retrieve_params(data):
    search_id = data.get('search_id')
    search_parameters = SearchParameters.objects.get(id=search_id) if search_id is not None else None

    crawl_parameters = CrawlParameters.from_dict(data['parameters'])
    return search_parameters, crawl_parameters


def send_message(component, channel_layer, where, message):
    logging.getLogger().info('[{0}] Sending message {1} to {2}'.format(component, message['type'], where))
    async_to_sync(channel_layer.send)(where, message)


def group_send_message(component, channel_layer, where, msg_type, message):
    logging.getLogger().info('[{0}] Sending message {1} to {2}'.format(component, msg_type, where))
    async_to_sync(channel_layer.group_send)(
        where,
        {
            'type': msg_type,
            'message': message
        }
    )
