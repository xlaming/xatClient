def command(core, packet, cmd, args, user):
    message = None

    if len(args) < 2:
        message = 'Please, tell me what is the user ID?'
    elif not args[1].isdigit():
        message = 'ID should be numeric...'
    else:
        usr = user.getById(int(args[1]))
        if not usr:
            message = 'User not found'
        else:
            message = '[%i] avatar\'s: %s' % (int(args[1]), usr['avatar'])

    user.announce(message)