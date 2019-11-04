def plugin(core, packet, direction, user):
    if direction == 'toxat' and packet['name'] == 'z':
        if packet['t'] != '/l':
            packet['t'] = '/a_NF'
        return packet
