def command(core, packet, cmd, args, user):
    message = None
    
    if len(args) < 2:
        message = 'Please, tell me what plugin should be enabled...'
    else:
        message = 'This plugin has been enabled' if core.enablePlugin(args[1]) else 'Plugin is already enabled or does not exist'

    user.announce(message)