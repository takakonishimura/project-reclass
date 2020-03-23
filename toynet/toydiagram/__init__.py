from toydiagram.network import ToySubnet, ToyNetDiagram
from toydiagram.nodes.switch import Switch
from toydiagram.nodes.host import Host
from toydiagram.nodes.router import Router
from toydiagram.diagramtree import DiagramTree

class ToyDiagram():
  def __init__(self, routers, switches, links):
    self.routers = routers
    self.switches = switches
    self.links = links

    diagramTree = DiagramTree(nodes={ 'routers': routers, 'switches': switches, 'links': links })
    self.subnets = diagramTree.getAllSubnets()


  def visualize(self):
    nodes = dict()
    with ToyNetDiagram("Toy Network", show=False):
        with ToySubnet("gateway"):
            for deviceName in self.routers:
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

        for (n1, n2) in self.links:
            nodes[n1] >> nodes[n2]
