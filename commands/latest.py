from requests import *
from json import loads

def command(core, packet, cmd, args, user):
    source = get('https://xatblog.net/api/latest?json')
    power = loads(source.content.decode('utf-8'))['result']

    smilies = ', '.join(power['smilies'])

    message = '[ID: %i] %s, price: %s, status: %s, smilies: %s' \
        % (int(power['id']), power['name'].upper(), power['price'], power['status'].capitalize(), smilies)

    user.announce(message)