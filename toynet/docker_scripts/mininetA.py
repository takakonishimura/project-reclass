#!/usr/bin/env python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import OVSController

class ToyTopo(Topo):
    "A LinuxRouter connecting three IP subnets"

    def build(self, **_opts):

        s = self.addSwitch("s0")

        h1 = self.addHost("h1", ip="192.168.2.1")
        h2 = self.addHost("h2", ip="192.168.2.2")

        self.addLink("s0", "h1")
        self.addLink("s0", "h2")

simpleTopo = ToyTopo()
net = Mininet(topo=simpleTopo,controller = OVSController)
net.start()
CLI( net )
