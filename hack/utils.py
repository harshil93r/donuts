import requests


def send_sms(message, contact, sender='DONUTS'):
    authKey = '103308AgoSro1T56a75435'
    raw_url = "http://control.msg91.com/api/sendhttp.php?authkey={authKey}&mobiles={contact}&message={message}&sender={sender}&route=4&country=91"

    formatted_url = raw_url.format(authKey=authKey,
                                   message=message,
                                   contact=contact,
                                   sender=sender)

    print(requests.get(formatted_url).text)
