from time import sleep

def command(core, packet, cmd, args, user):
    user.announce('Ok, you need to press Sign Out then Sign In.')
    sleep(2)
    user.sendToXat(core.buildPacket('v', {'p': 0, 'n': user.userID}))