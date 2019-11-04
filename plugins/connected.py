def plugin(core, packet, direction, user):
    if direction == 'fromxat' and packet['name'] == 'done':
        user.send(core.buildPacket('m', {'t': 'xatClient is working...', 'u': 0}))