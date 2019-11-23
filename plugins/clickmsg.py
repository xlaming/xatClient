def plugin(core, packet, direction, user):
    if direction == 'fromxat' and packet['name'] == 'z':
        if packet['t'] == '/l':
            userID = core.fixUserID(packet['u'])
            user.announce(str(userID) + ' has ticked you')