from toynet.toytopo import ToyTopo
from toydiagram.diagramTree import DiagramTree, DiagramGraph
from toydiagram.network import ToyNetDiagram, ToySubnet, ToyNetNode
from toydiagram.nodes.switch import Switch
from toydiagram.nodes.host import Host
from toydiagram.nodes.router import Router

from mininet.net import Mininet
from mininet.cli import CLI

class ToyNet():
    def __init__(self, topology=ToyTopo()):
        self.mininet = Mininet(topo=topology)

        print('__INFO___ Generating Diagram Graph from Configurations')
        graph = DiagramGraph(self.deviceNamesByType(), 'risp')

        print('__INFO___ Generating Diagram Tree from Diagram Graph')
        self.diagramTree = graph.getDiagramTree()

        print('routers: ' + str(self.diagramTree.routers))
        print('free: ' + str(self.diagramTree.freeNodes))
        print('primary: ' + str(self.diagramTree.primaryLinks))
        print('secondary: ' + str(self.diagramTree.secondaryLinks))
        print('unused: ' + str(self.diagramTree.unusedLinks))
        print('')
        for i, subnet in enumerate(self.diagramTree.subnets):
            print('----subnet ' + str(i) + ':')
            print('----switches: ' + str(subnet.switches))
            print('----hosts: ' + str(subnet.hosts))
            print('')


    def visualize(self):
        nodes = dict()
        with ToyNetDiagram("Toy Network", show=False):

            # devices
            for deviceName in self.diagramTree.routers:
                nodes[deviceName] = Router(deviceName)

            for (i, subnet) in enumerate(self.diagramTree.subnets):
                with ToySubnet("subnet" + str(i)):
                    for deviceName in subnet.switches:
                            nodes[deviceName] = Switch(deviceName)
                    for deviceName in subnet.hosts:
                            nodes[deviceName] = Host(deviceName)

            # cables
            for (n1, n2) in self.diagramTree.primaryLinks:
                nodes[n1] >> nodes[n2]

            for (n1, n2) in self.diagramTree.secondaryLinks:
                nodes[n1] >> nodes[n2]

    def interact(self):
        self.mininet.start()
        CLI( self.mininet )
        self.mininet.stop()

    def deviceNamesByType(self):
        devices = {
            'routers': list(),
            'switches': [s.name for s in self.mininet.switches if s.name.startswith('s')],
            'hosts': list(),
            'links': [(l.intf1.node.name, l.intf2.node.name) for l in self.mininet.links]
        }

        for device in self.mininet.hosts:
            if device.name.startswith('r'): devices['routers'].append(device.name)
            elif device.name.startswith('h'): devices['hosts'].append(device.name)

        return devices