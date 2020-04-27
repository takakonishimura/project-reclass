from toynet.toytopo import ToyTopo
from toydiagram.network import ToyNetDiagram, ToySubnet, ToyNetNode
from toydiagram.nodes.switch import Switch
from toydiagram.nodes.host import Host
from toydiagram.nodes.router import Router
from toydiagram.diagramtree import DiagramTree

from mininet.net import Mininet
from mininet.cli import CLI

class ToyNet():
  def __init__(self, topology=ToyTopo()):
    self.mininet = Mininet(topo=topology)

    self.nodes = {
      'routers': self.getRouterNames(),
      'switches': self.getSwitchNames(),
      'links': self.getLinkPairs()
    }

    diagramTree = DiagramTree(self.nodes)
    self.subnets = diagramTree.getAllSubnets()


  def visualize(self):
    nodes = dict()
    with ToyNetDiagram("Toy Network", show=False):
        with ToySubnet("gateway"):
            for deviceName in self.nodes['routers']:
                nodes[deviceName] = Router(deviceName)

        for subnet in self.subnets:
            with ToySubnet(subnet[0]):
                for deviceName in subnet:
                    if deviceName.startswith('s'):
                        nodes[deviceName] = Switch(deviceName)
                    elif deviceName.startswith('h'):
                        nodes[deviceName] = Host(deviceName)
                    else:
                        print('device is neither a switch nor a router: ', deviceName)
                        # exception?

        for (n1, n2) in self.nodes['links']:
            nodes[n1] >> nodes[n2]

  def interact(self):
    self.mininet.start()
    CLI( self.mininet )
    self.mininet.stop()

  def getRouterNames(self):
    return [h.name for h in self.mininet.hosts if h.name.startswith('r')]

  def getSwitchNames(self):
    return [s.name for s in self.mininet.switches if s.name.startswith('s')]

  def getLinkPairs(self):
    return [(l.intf1.node.name, l.intf2.node.name) for l in self.mininet.links]