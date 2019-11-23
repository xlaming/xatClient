from requests import *

def command(core, packet, cmd, args, user):
    message = None

    if len(args) < 2:
        message = 'Please, tell me what is the chat name...'
    else:
        source = get('https://api.mundosmilies.com/chatid/' + args[1]).content
        if source == b'nope':
            message = 'Chat not found'
        else:
            message = '[%s] chat ID: %i' % (args[1], int(source))

    user.announce(message)