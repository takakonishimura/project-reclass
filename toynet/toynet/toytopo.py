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

        rISP_IP_0 = '192.168.0.1/24'  # IP address for risp-eth0
        rISP_IP_1 = '192.168.1.1/24'  # IP address for risp-eth1
        rISP_IP_2 = '192.168.2.1/24'  # IP address for risp-eth2
        routerISP = self.addNode('risp', cls=LinuxRouter, ip=rISP_IP_0)

        r1_IP_0 = '192.168.1.1/24'  # IP address for r1-eth0
        r1_IP_1 = '192.168.1.2/24'  # IP address for r1-eth1
        r1 = self.addNode('r1', cls=LinuxRouter, ip=r1_IP_0)

        r2_IP_0 = '172.16.0.1/12'  # IP address for r2-eth0
        r2_IP_1 = '172.16.0.2/12'  # IP address for r2-eth1
        r2 = self.addNode('r2', cls=LinuxRouter, ip=r2_IP_0)

        s1, s2, s3, s4 = [self.addSwitch(s) for s in ('s1', 's2', 's3', 's4')]

        self.addLink(routerISP, r1, intfName1='risp-eth1', intfName2='r1-eth0',
                     params1={'ip': rISP_IP_1}, params2={'ip': r1_IP_1})  # for clarity
        self.addLink(routerISP, r2, intfName1='risp-eth2', intfName2='r2eth0',
                     params1={'ip': rISP_IP_2}, params2={'ip': r1_IP_1})  # for clarity
        self.addLink(r1, s1, intfName1='r1-eth1', intfName2='s1-eth0',
                     params1={'ip': r1_IP_1})  # for clarity
        self.addLink(r2, s2, intfName1='r2-eth1', intfName2='s2-eth0',
                     params1={'ip': r2_IP_1})
        self.addLink(s2, s3, intfName1='s2-eth1', intfName2='s3-eth0')
        self.addLink(s2, s4, intfName1='s2-eth2', intfName2='s4-eth0')

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
