import netifaces

def get_ip(remote_addr='127.0.0.1'):

    if remote_addr != '127.0.0.1':

        return remote_addr

    

    for interface in netifaces.interfaces():

        addrs = netifaces.ifaddresses(interface)

        if netifaces.AF_INET in addrs:

            for addr in addrs[netifaces.AF_INET]:

                if 'addr' in addr:

                    ip = addr['addr']

                    if not ip.startswith('127.'):

                        return ip

    

    return '127.0.0.1'

