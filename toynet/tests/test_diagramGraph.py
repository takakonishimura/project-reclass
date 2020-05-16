import unittest

from toydiagram.diagramTree import DiagramGraph, DeviceType
from util.error import DiagramGraphError, TypeCheckError

class TestDiagramGraphMethods(unittest.TestCase):

    def test_DiagramGraph__basicCreation_router(self):
        nodes = {
            'routers': ['r'],
            'switches': [],
            'hosts': [],
            'links': []
        }
        graph = DiagramGraph(nodes)

        self.assertTrue(hasattr(graph,'root'))
        self.assertEqual(graph.devices['r'], graph.root)
        self.assertEqual(graph.root.deviceType, DeviceType.ROUTER)
        self.assertEqual(graph.root.deviceName, 'r')
        self.assertEqual(len(graph.devices.keys()), 1)

    def test_DiagramGraph__basicCreation_switch(self):
        nodes = {
            'routers': [],
            'switches': ['s'],
            'hosts': [],
            'links': []
        }
        graph = DiagramGraph(nodes)

        self.assertTrue(hasattr(graph,'root'))
        self.assertEqual(graph.devices['s'], graph.root)
        self.assertEqual(graph.root.deviceType, DeviceType.SWITCH)
        self.assertEqual(graph.root.deviceName, 's')
        self.assertEqual(len(graph.devices.keys()), 1)

    def test_DiagramGraph__basicCreation_host(self):
        nodes = {
            'routers': [],
            'switches': [],
            'hosts': ['h'],
            'links': []
        }
        graph = DiagramGraph(nodes)

        self.assertFalse(hasattr(graph,'root'))
        self.assertEqual(len(graph.devices.keys()), 1)
        self.assertEqual(graph.devices['h'].deviceName, 'h')
        self.assertEqual(graph.devices['h'].deviceType, DeviceType.HOST)

    def test_DiagramGraph__badCreation_noDevices(self):
        nodes = {
            'routers': [],
            'switches': [],
            'hosts': [],
            'links': []
        }
        
        with self.assertRaises(DiagramGraphError) as cm:
            DiagramGraph(nodes)
        self.assertEqual(cm.exception.message, 'network is missing devices')

    def test_DiagramGraph__routersCreation_links(self):
        nodes = {
            'routers': ['r1', 'r2', 'r3'],
            'switches': [],
            'hosts': [],
            'links': [('r1', 'r2'), ('r1', 'r3')]
        }
        graph = DiagramGraph(nodes)

        self.assertEqual(len(graph.devices.keys()), 3)
        self.assertEqual(len(graph.devices['r1'].neighbors), 2)
        self.assertEqual(len(graph.devices['r2'].neighbors), 1)
        self.assertEqual(len(graph.devices['r3'].neighbors), 1)
        
    def test_DiagramGraph__routersCreation_dupLink(self):
        nodes = {
            'routers': ['r1', 'r2', 'r3'],
            'switches': [],
            'hosts': [],
            'links': [('r1', 'r2'), ('r1', 'r2'),]
        }
        graph = DiagramGraph(nodes)

        self.assertEqual(len(graph.devices.keys()), 3)
        self.assertEqual(len(graph.devices['r1'].neighbors), 1)
        self.assertEqual(len(graph.devices['r2'].neighbors), 1)
        self.assertEqual(len(graph.devices['r3'].neighbors), 0)

    def test_DiagramGraph__routersCreation_badLink(self):
        nodes = {
            'routers': ['r1', 'r2', 'r3'],
            'switches': [],
            'hosts': [],
            'links': [('r1', 'r0'),]
        }

        with self.assertRaises(DiagramGraphError) as cm:
            graph = DiagramGraph(nodes)
        self.assertEqual(cm.exception.message, 'Device r0 not found in Graph devices')

    def test_DiagramGraph__routersCreation_triangle(self):
        nodes = {
            'routers': ['r1', 'r2', 'r3'],
            'switches': [],
            'hosts': [],
            'links': [('r1', 'r2'), ('r1', 'r3'), ('r2', 'r3')]
        }
        graph = DiagramGraph(nodes)

        self.assertEqual(len(graph.devices.keys()), 3)
        self.assertEqual(len(graph.devices['r1'].neighbors), 2)
        self.assertEqual(len(graph.devices['r2'].neighbors), 2)
        self.assertEqual(len(graph.devices['r3'].neighbors), 2)