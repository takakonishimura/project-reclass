#!/usr/bin/env python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import OVSController

class ToyTopo(Topo):
    "A LinuxRouter connecting three IP subnets"

    def build(self, **_opts):

        s = self.addSwitch("s0")

        h3 = self.addHost("h1", ip="192.168.2.3")
        h4 = self.addHost("h2", ip="192.168.2.4")

        self.addLink("s0", "h3")
        self.addLink("s0", "h4")

simpleTopo = ToyTopo()
net = Mininet(topo=simpleTopo,controller = OVSController)
net.start()
CLI( net )
