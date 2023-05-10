import subprocess
import re

#172.20.10.2 via 172.31.32.1 dev eth0 src 172.31.35.207 uid 0 \ cache
#192.168.122.1 dev enp1s0 src 192.168.122.140 uid 0 \    cache

class NetConsoleParams(object):
    def __init__(self, remote_ip, dev_name=None, local_ip=None,
                 local_port=6665, remote_port=6666,
                 remote_mac=None):

        super(NetConsoleParams, self).__init__()

        route=['ip', '-o', 'route', 'get', remote_ip]
        self.route_output = subprocess.check_output(route).decode()

        self.dev_name = dev_name

        self.local_ip = local_ip
        self.remote_ip = remote_ip

        self.local_port = local_port
        self.remote_port = remote_port

        self.remote_mac = remote_mac

    def __str__(self):
        self.get_module_params()
        return "dev_name: {}, local_ip: {}, local_port: {}, "\
                "remote_ip: {}, remote_port: {}, remote_mac: {}".format(
            self.dev_name,  self.local_ip,    self.local_port,
            self.remote_ip, self.remote_port, self.remote_mac);

    def __repr__(self):
        self.get_module_params()
        return "{}, {}, {}, {}, {}, {}".format(
            type(self.dev_name),  type(self.local_ip),    type(self.local_port),
            type(self.remote_ip), type(self.remote_port), type(self.remote_mac));

    def _parse_dev_name_from_route_output(self):
        match=re.search(r'dev [^ ]*', self.route_output)
        self.dev_name = match.group().split()[1]

    def get_dev_name(self):
        if self.dev_name is None:
            self._parse_dev_name_from_route_output()

        return self.dev_name

    def _parse_local_ip_from_route_output(self):
        match = re.search(r'src [^ ]*', self.route_output)
        self.local_ip = match.group().split()[1]

    def get_local_ip(self):
        if self.local_ip is None:
            self._parse_local_ip_from_route_output()

        return self.local_ip

    def _parse_remote_mac_from_route_output(self):
        match=re.search(r'via [^ ]*', self.route_output)

        if match:
            gateway=match.group().split()[1]
        else:
            gateway=self.remote_ip

        mac_command = ['ip', '-o', 'neigh', 'show', 'to', gateway, 'dev', self.dev_name]
        mac_output = subprocess.check_output(mac_command).decode()
        match = re.search(r'lladdr [^ ]*', mac_output)
        if match is not None:
            self.remote_mac = match.group().split()[1]
        else:
            raise Exception("There is no route to remote host. "\
                            "Can't calculate remote mac")

    def get_remote_mac(self):
        if self.remote_mac is None:
            self._parse_remote_mac_from_route_output()

        return self.remote_mac

    def get_remote_ip(self):
        return self.remote_ip

    def get_local_port(self):
        return self.local_port

    def get_remote_port(self):
        return self.remote_port

    def get_module_params(self):
        return {
            'dev_name': self.get_dev_name(),
            'local_ip': self.get_local_ip(),
            'local_port': self.get_local_port(),
            'remote_port': self.get_remote_port(),
            'remote_ip': self.get_remote_ip(),
            'remote_mac': self.get_remote_mac() }
        
    def set_dev_name(self, dev_name):
        self.dev_name = dev_name

    def set_local_ip(self, local_ip):
        self.local_ip = local_ip

    def set_remote_ip(self, remote_ip):
        self.remote_ip = remote_ip

    def set_local_port(self, local_port):
        self.local_port = local_port

    def set_remote_port(self, remote_port):
        self.remote_port = remote_port

    def set_remote_mac(self, remote_mac):
        self.remote_mac = remote_mac

        
if __name__ == "__main__":
    nparams = NetConsoleParams('192.168.122.1')
    print(str(nparams), repr(nparams))
