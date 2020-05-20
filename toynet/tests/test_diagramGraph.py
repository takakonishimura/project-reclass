import unittest

from toydiagram.diagramTree import DiagramGraph, DeviceType
from util.error import DiagramGraphError

import tests.util as testutil

class TestDiagramGraphMethods(unittest.TestCase):

    def test_DiagramGraph__basicCreation_router(self):
        config = testutil.makeToyTopoConfig(
            ['r'],  # routers
            [],     # switches
            [],     # hosts
            []      # links
        )
        graph = DiagramGraph(config)

        self.assertTrue(hasattr(graph,'root'))
        self.assertEqual(graph.devices['r'], graph.root)
        self.assertEqual(graph.root.deviceType, DeviceType.ROUTER)
        self.assertEqual(graph.root.deviceName, 'r')
        self.assertEqual(len(graph.devices.keys()), 1)

    def test_DiagramGraph__basicCreation_switch(self):
        config = testutil.makeToyTopoConfig(
            [],     # routers
            ['s'],  # switches
            [],     # hosts
            []      # links
        )
        graph = DiagramGraph(config)

        self.assertTrue(hasattr(graph,'root'))
        self.assertEqual(graph.devices['s'], graph.root)
        self.assertEqual(graph.root.deviceType, DeviceType.SWITCH)
        self.assertEqual(graph.root.deviceName, 's')
        self.assertEqual(len(graph.devices.keys()), 1)

    def test_DiagramGraph__basicCreation_host(self):
        config = testutil.makeToyTopoConfig(
            [],     # routers
            [],     # switches
            ['h'],  # hosts
            []      # links
        )
        graph = DiagramGraph(config)

        self.assertIsNone(graph.root)
        self.assertEqual(len(graph.devices.keys()), 1)
        self.assertEqual(graph.devices['h'].deviceName, 'h')
        self.assertEqual(graph.devices['h'].deviceType, DeviceType.HOST)

    def test_DiagramGraph__badCreation_noDevices(self):
        config = testutil.makeToyTopoConfig(
            [],     # routers
            [],     # switches
            [],     # hosts
            []      # links
        )
        
        with self.assertRaises(DiagramGraphError) as cm:
            DiagramGraph(config)
        self.assertEqual(cm.exception.message, 'network is missing devices')

    def test_DiagramGraph__routersCreation_links(self):
        config = testutil.makeToyTopoConfig(
            ['r1', 'r2', 'r3'],             # routers
            [],                             # switches
            [],                             # hosts
            [('r1', 'r2'), ('r1', 'r3')]    # links
        )
        graph = DiagramGraph(config)

        self.assertEqual(len(graph.devices.keys()), 3)
        self.assertEqual(len(graph.devices['r1'].neighbors), 2)
        self.assertEqual(len(graph.devices['r2'].neighbors), 1)
        self.assertEqual(len(graph.devices['r3'].neighbors), 1)
        
    def test_DiagramGraph__routersCreation_dupLink(self):
        config = testutil.makeToyTopoConfig(
            ['r1', 'r2', 'r3'],             # routers
            [],                             # switches
            [],                             # hosts
            [('r1', 'r2'), ('r1', 'r2')]    # links
        )
        graph = DiagramGraph(config)

        self.assertEqual(len(graph.devices.keys()), 3)
        self.assertEqual(len(graph.devices['r1'].neighbors), 1)
        self.assertEqual(len(graph.devices['r2'].neighbors), 1)
        self.assertEqual(len(graph.devices['r3'].neighbors), 0)

    def test_DiagramGraph__routersCreation_badLink(self):
        config = testutil.makeToyTopoConfig(
            ['r1', 'r2', 'r3'],     # routers
            [],                     # switches
            [],                     # hosts
            [('r1', 'r0')]          # links
        )

        with self.assertRaises(DiagramGraphError) as cm:
            DiagramGraph(config)
        self.assertEqual(cm.exception.message, 'Device r0 not found in Graph devices')

    def test_DiagramGraph__routersCreation_routerHost(self):
        config = testutil.makeToyTopoConfig(
            ['r1'],             # routers
            [],                 # switches
            ['h1'],             # hosts
            [('r1', 'h1')]      # links
        )

        with self.assertRaises(DiagramGraphError) as cm:
            DiagramGraph(config)
        self.assertEqual(cm.exception.message, 'Device type ROUTER cannot be neighbors with HOST (Entity: r1 [ROUTER, 0 neighbors])')


    def test_DiagramGraph__routersCreation_triangle(self):
        config = testutil.makeToyTopoConfig(
            ['r1', 'r2', 'r3'],                         # routers
            [],                                         # switches
            [],                                         # hosts
            [('r1', 'r2'), ('r1', 'r3'), ('r2', 'r3')]  # links
        )
        graph = DiagramGraph(config)

        self.assertEqual(len(graph.devices.keys()), 3)
        self.assertEqual(len(graph.devices['r1'].neighbors), 2)
        self.assertEqual(len(graph.devices['r2'].neighbors), 2)
        self.assertEqual(len(graph.devices['r3'].neighbors), 2)