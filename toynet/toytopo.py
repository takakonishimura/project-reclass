from mininet.node import Node
from mininet.topo import Topo

# To see Routing Table on a Router: print( net[ 'r0' ].cmd( 'route' ) )
# These classes are copied from examples/linuxrouter.py and modified


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class ToyTopo(Topo):
    "A LinuxRouter connecting three IP subnets"

    def build(self, **_opts):

        defaultIP = '192.168.1.1/24'  # IP address for r0-eth1
        router = self.addNode('r0', cls=LinuxRouter, ip=defaultIP)

        s1, s2, s3, s4 = [self.addSwitch(s) for s in ('s1', 's2', 's3', 's4')]

        self.addLink(router, s1, intfName2='r0-eth1',
                     params2={'ip': defaultIP})  # for clarity
        self.addLink(router, s2, intfName2='r0-eth2',
                     params2={'ip': '172.16.0.1/12'})
        # TODO @taytay: diagram flow is awkward when parameters are reversed
        self.addLink(s2, s3)
        self.addLink(s2, s4)

        h1 = self.addHost('h1', ip='192.168.1.100/24',
                          defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2', ip='172.16.0.100/12',
                          defaultRoute='via 172.16.0.1')
        h3 = self.addHost('h3', ip='172.16.0.101/12',
                          defaultRoute='via 10.0.0.1')
        h4 = self.addHost('h4', ip='172.16.0.102/12',
                          defaultRoute='via 20.0.0.1')

        for s, h in [(s1, h1), (s1, h2), (s3, h3), (s4, h4)]:
            self.addLink(s, h)
