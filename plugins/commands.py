from os import path
from classes.config import Config

def plugin(core, packet, direction, user):
    if direction == 'toxat' and packet['name'] == 'm':
        userID = core.fixUserID(packet['u'])
        args = packet['t'].split(' ', 1)
        cmd = args[0][1:].lower()
        cc = args[0][0]

        if "s" in packet:
            return
        elif cc != Config.CMD_CHARACTER:
            return

        if path.exists('commands/' + cmd + '.py'):
            exec(open('commands/' + cmd + '.py').read(), globals())
            command(core, packet, userID, cmd, args, user)
        else:
            user.send(core.buildPacket('m', {'t': 'Command not found!', 'u': 0}))       

        packet['name'] = 'HIDDEN' # my message won't be sent

        return packet