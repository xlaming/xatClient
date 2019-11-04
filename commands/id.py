from requests import *
from json import loads

def command(core, packet, uid, cmd, args, user):
    message = None

    if len(args) < 2:
        message = 'Please, tell me what is the xat username...'
    else:
        source = get('https://xatblog.net/api/reg2id/%s?json' % args[1])
        result = loads(source.content.decode('utf-8'))['result']
        if type(result) is not int:
            message = 'User not found.'
        else:
            message = '[%s] user ID: %i' % (args[1], result)

    user.send(core.buildPacket('m', {'t': message, 'u': 0}))