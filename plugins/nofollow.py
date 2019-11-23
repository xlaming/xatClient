def plugin(core, packet, direction, user):
    if direction == 'toxat' and packet['name'] == 'z':
        if packet['t'][:2] == '/a':
            packet['t'] = '/a_NF'