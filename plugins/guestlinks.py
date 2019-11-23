def plugin(core, packet, direction, user):
    if direction == 'fromxat' and packet['name'] == 'm' and 'u' in packet and 'l' in packet:
        uID = int(core.fixUserID(packet['u']))
        usr = user.getById(uID)
        if usr['rank'] >= 5 or usr['rank'] == 0:
            user.announce('Guest [%i]: %s' % (uID, packet['t']))