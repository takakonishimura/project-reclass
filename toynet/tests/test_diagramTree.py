import unittest

from toydiagram.diagramTree import DiagramGraph, DeviceType
from util.error import DiagramGraphError, TypeCheckError

class TestDiagramTreeMethods(unittest.TestCase):
    def test_DiagramTree__basicCreation_router(self):
        nodes = {
            'routers': ['r'],
            'switches': [],
            'hosts': [],
            'links': []
        }
        graph = DiagramGraph(nodes)
        tree = graph.getDiagramTree()
        fr = tree.freeNodes

        self.assertEqual(len(tree.routers), 1)
        self.assertEqual(len(tree.subnets), 0)
        self.assertEqual(len(fr['routers']) + len(fr['switches']) + len(fr['hosts']), 0)
        self.assertEqual(len(tree.primaryLinks), 0)
        self.assertEqual(len(tree.secondaryLinks), 0)
        self.assertEqual(len(tree.redundantLinks), 0)
        self.assertEqual(len(tree.unusedLinks), 0)

    def test_DiagramTree__basicCreation_routerroot(self):
        nodes = {
            'routers': ['r'],
            'switches': [],
            'hosts': [],
            'links': []
        }
        graph = DiagramGraph(nodes, 'r')
        tree = graph.getDiagramTree()
        fr = tree.freeNodes

        self.assertEqual(len(tree.routers), 1)
        self.assertEqual(len(tree.subnets), 0)
        self.assertEqual(len(fr['routers']) + len(fr['switches']) + len(fr['hosts']), 0)
        self.assertEqual(len(tree.primaryLinks), 0)
        self.assertEqual(len(tree.secondaryLinks), 0)
        self.assertEqual(len(tree.redundantLinks), 0)
        self.assertEqual(len(tree.unusedLinks), 0)

    def test_DiagramTree__basicCreation_badroot(self):
        nodes = {
            'routers': ['r'],
            'switches': [],
            'hosts': [],
            'links': []
        }
        graph = DiagramGraph(nodes, 'r0')
        tree = graph.getDiagramTree()
        fr = tree.freeNodes

        self.assertEqual(len(tree.routers), 1)
        self.assertEqual(len(tree.subnets), 0)
        self.assertEqual(len(fr['routers']) + len(fr['switches']) + len(fr['hosts']), 0)
        self.assertEqual(len(tree.primaryLinks), 0)
        self.assertEqual(len(tree.secondaryLinks), 0)
        self.assertEqual(len(tree.redundantLinks), 0)
        self.assertEqual(len(tree.unusedLinks), 0)

    def test_DiagramTree__routersCreation_zlink(self):
        nodes = {
            'routers': ['r1', 'r2', 'r3'],
            'switches': [],
            'hosts': [],
            'links': [('r1', 'r2')]
        }
        graph = DiagramGraph(nodes)
        tree = graph.getDiagramTree()
        fr = tree.freeNodes

        self.assertEqual(len(tree.routers), 2)
        self.assertEqual(len(tree.subnets), 0)
        self.assertEqual(len(fr['routers']), 1)
        self.assertEqual(len(fr['switches']) + len(fr['hosts']), 0)
        self.assertEqual(len(tree.primaryLinks), 1)
        self.assertEqual(len(tree.secondaryLinks), 0)
        self.assertEqual(len(tree.redundantLinks), 2)
        self.assertEqual(len(tree.unusedLinks), 0)

    def test_DiagramTree__subnetCreation_basic(self):
        nodes = {
            'routers': ['r1', 'r2'],
            'switches': ['s1'],
            'hosts': [],
            'links': [('r1', 'r2'), ('r1', 's1')]
        }
        graph = DiagramGraph(nodes)
        tree = graph.getDiagramTree()
        fr = tree.freeNodes

        self.assertEqual(len(tree.routers), 2)
        self.assertEqual(len(tree.subnets), 1)
        self.assertEqual(len(tree.subnets[0].switches), 1)
        self.assertEqual(len(tree.subnets[0].hosts), 0)
        self.assertEqual(len(fr['routers']) + len(fr['switches']) + len(fr['hosts']), 0)
        self.assertEqual(len(tree.primaryLinks), 2)
        self.assertEqual(len(tree.secondaryLinks), 0)
        self.assertEqual(len(tree.redundantLinks), 4)
        self.assertEqual(len(tree.unusedLinks), 0)
