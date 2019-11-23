def command(core, packet, cmd, args, user):
    message = None
    
    if len(args) < 2:
        message = 'Please, tell me what plugin should be disabled...'
    else:
        message = 'This plugin has been disabled' if core.disablePlugin(args[1]) else 'Plugin is already disabled or does not exist'

    user.announce(message)