from requests import *
from json import loads

def command(core, packet, uid, cmd, args, user):
    message = None

    if len(args) < 2:
        message = 'Please, tell me what is the power name...'
    else:
        source = get('http://xatproject.com/fairtrade/api.php?action=search_power&power=%s' % args[1])
        result = loads(source.content.decode('utf-8'))
        if result['status'] == 'fail':
            message = 'Power not found.'
        else:
            power = result['power']
            message = '[ID: %i] %s %i-%i xats or %i-%i days on FairTrade' \
                % (power['id'], power['name'].upper(), power['min_xats'], power['max_xats'], power['min_days'], power['max_days'])

    user.send(core.buildPacket('m', {'t': message, 'u': 0}))