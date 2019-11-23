from os import path
from classes.config import Config

def plugin(core, packet, direction, user):
    if direction == 'toxat' and packet['name'] == 'm':
        args = packet['t'].split(' ', 1)
        cmd = args[0][1:].lower()
        cc = args[0][:1]

        if "s" in packet:
            return
        elif cc != Config.CMD_CHARACTER:
            return

        if path.exists('commands/' + cmd + '.py'):
            exec(open('commands/' + cmd + '.py').read(), globals())
            command(core, packet, cmd, args, user)
        else: 
            user.announce('Command not found')  

        packet['name'] = 'HIDDEN' # my packet is now hidden
