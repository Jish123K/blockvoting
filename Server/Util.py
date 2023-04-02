import netifaces

def get_ip(remote_addr='127.0.0.1'):

    if remote_addr != '127.0.0.1':

        return remote_addr

    interfaces = netifaces.interfaces()

    for interface in interfaces:

        ifaddresses = netifaces.ifaddresses(interface)

        if netifaces.AF_INET in ifaddresses:

            addresses = ifaddresses[netifaces.AF_INET]

            for address in addresses:

                ip = address.get('addr')

                if ip and not ip.startswith('127.'):

                    return ip

    return '127.0.0.1'

