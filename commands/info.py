def command(core, packet, uid, cmd, args, user):
    user.send(core.buildPacket('m', {'t': 'xatClient by xLaming.', 'u': 0}))