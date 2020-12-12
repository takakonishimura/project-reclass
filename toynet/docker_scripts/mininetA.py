from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI

simpleTopo = ToyTopo()
net = Mininet(topo=simpleTopo)
net.start()
CLI( net )

class ToyTopo(Topo):
    "A LinuxRouter connecting three IP subnets"

    def build(self, config:ToyTopoConfig, **_opts):

        s = self.addSwitch("s0")

        h1 = self.addHost("h1", ip="192.168.2.1")
        h2 = self.addHost("h2", ip="192.168.2.2")

        self.addLink("s0", "h1")
        self.addLInk("s0", "h2")
