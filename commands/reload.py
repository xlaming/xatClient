def command(core, packet, uid, cmd, args, user):
    core.loadPlugins()
    user.send(core.buildPacket('m', {'t': 'Plugins has been reloaded.', 'u': 0}))
