from requests import *
from json import loads

def command(core, packet, cmd, args, user):
    message = None

    if len(args) < 2:
        message = 'Please, tell me what is the xat ID...'
    else:
        source = get('https://xatblog.net/api/id2reg/%s?json' % args[1])
        result = loads(source.content.decode('utf-8'))['result']
        if type(result) is not str:
            message = 'User not found'
        else:
            message = '[%i] username: %s' % (int(args[1]), result)

    user.announce(message)