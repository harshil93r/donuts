import requests
from django.conf import settings

def send_sms(message, contact, sender='DONUTS'):
    authKey = '103308AgoSro1T56a75435'
    raw_url = "http://control.msg91.com/api/sendhttp.php?authkey={authKey}&mobiles={contact}&message={message}&sender={sender}&route=4&country=91"

    formatted_url = raw_url.format(authKey=authKey,
                                   message=message,
                                   contact=contact,
                                   sender=sender)

    print(requests.get(formatted_url).text)


def notify(data, channel):
    '''
    Publish to given socket channel with data provided.
    Params:
        data    : dict to be published
        channel : channel id at which the data is to be published
    '''
    if not isinstance(channel, str):
        channel = str(channel)
    base_uri = '{websocket}/pub?id='.format(
        websocket=settings.WEBSOCKET_ADDR)
    url = base_uri + channel

    print(requests.post(url, json=data).text, channel)
