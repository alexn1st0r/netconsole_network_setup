import subprocess
import re

#172.20.10.2 via 172.31.32.1 dev eth0 src 172.31.35.207 uid 0 \ cache
#192.168.122.1 dev enp1s0 src 192.168.122.140 uid 0 \    cache

def get_mac_address_from_ip(address, dev_name):
    mac_command = ['ip', '-o', 'neigh', 'show', 'to', address, 'dev', dev_name]
    mac_output = subprocess.check_output(mac_command).decode()
    match=re.search(r'lladdr [^ ]*', mac_output)

    return match.group().split(" ")[1]


def get_full_address_from_remote_ip(remote_ip):
    route=['ip', '-o', 'route', 'get', remote_ip]
    route_output = subprocess.check_output(route).decode()

    match=re.search(r'dev [^ ]*', route_output)
    dev_name = match.group().split()[1]

    match=re.search(r'src [^ ]*', route_output)
    local_ip=match.group().split()[1]

    match=re.search(r'via [^ ]*', route_output)

    if match:
        gateway=match.group().split()[1]
    else:
        gateway=remote_ip

    mac = get_mac_address_from_ip(gateway, dev_name)

    return {
            'dev_name': dev_name,
            'local_ip': local_ip,
            'remote_ip': remote_ip,
            'remote_mac': mac }

if __name__ == "__main__":
    print(get_full_address_from_remote_ip('192.168.122.1'))
