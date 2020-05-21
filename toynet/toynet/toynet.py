from toynet.toytopo import ToyTopo
import toynet.xmlParser as parser
from toynet.xmlParser import ToyTopoConfig

from toydiagram.diagramTree import DiagramGraph
from toydiagram.network import ToyNetDiagram, ToySubnet
from toydiagram.nodes.switch import Switch
from toydiagram.nodes.host import Host
from toydiagram.nodes.router import Router

from mininet.net import Mininet
from mininet.cli import CLI


class ToyNet():
    def __init__(self, filename:str):
        self.config:ToyTopoConfig = parser.parseXML(filename)

    def visualize(self, title:str):
        print('__INFO___ Generating Diagram Graph from Configurations')
        graph = DiagramGraph(self.config)
        print('__INFO___ Generating Diagram Tree from Diagram Graph')
        self.diagramTree = graph.getDiagramTree()

        print(self.diagramTree.toString())

        nodes = dict()
        with ToyNetDiagram(title, show=False):

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

        return title.lower().replace(' ', '_') + '.png'

    def interact(self):
        print('__INFO___ Generating Interactive Mininet Instance')
        topology=ToyTopo(self.config) # ToyNet( topo=TreeTopo( depth=2, fanout=6 ) )
        self.mininet = Mininet(topo=topology)

        self.mininet.start()
        CLI( self.mininet )
        self.mininet.stop()
