import unittest

from toydiagram.diagramTree import DiagramGraph
from util.error import DiagramGraphError

import tests.util as testutil

class TestDiagramTreeMethods(unittest.TestCase):
    def test_DiagramTree__basicCreation_router(self):
        config = testutil.makeToyTopoConfig(
            ['r'],  # routers
            [],     # switches
            [],     # hosts
            []      # links
        )
        graph = DiagramGraph(config)
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
        config = testutil.makeToyTopoConfig(
            ['r'],  # routers
            [],     # switches
            [],     # hosts
            [],     # links
            'r'     # root
        )
        graph = DiagramGraph(config)
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
        config = testutil.makeToyTopoConfig(
            ['r'],  # routers
            [],     # switches
            [],     # hosts
            [],     # links
            'r0'    # root
        )
        graph = DiagramGraph(config)
        tree = graph.getDiagramTree()
        fr = tree.freeNodes

        self.assertEqual(len(tree.routers), 1)
        self.assertEqual(len(tree.subnets), 0)
        self.assertEqual(len(fr['routers']) + len(fr['switches']) + len(fr['hosts']), 0)
        self.assertEqual(len(tree.primaryLinks), 0)
        self.assertEqual(len(tree.secondaryLinks), 0)
        self.assertEqual(len(tree.redundantLinks), 0)
        self.assertEqual(len(tree.unusedLinks), 0)

    def test_DiagramTree__routersCreation_link(self):
        config = testutil.makeToyTopoConfig(
            ['r1', 'r2', 'r3'],     # routers
            [],                     # switches
            [],                     # hosts
            [('r1', 'r2')],         # links
            'r'                     # root
        )
        graph = DiagramGraph(config)
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
        config = testutil.makeToyTopoConfig(
            ['r1', 'r2'],                   # routers
            ['s1'],                         # switches
            [],                             # hosts
            [('r1', 'r2'), ('r1', 's1')]    # links
        )
        graph = DiagramGraph(config)
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

    def test_DiagramTree__subnetCreation_basic(self):
        config = testutil.makeToyTopoConfig(
            ['r0', 'r1', 'r2'],             # routers
            ['s1', 's2', 's3', 's4'],       # switches
            ['h1', 'h2', 'h3', 'h4', 'h5'], # hosts

            # links
            [('r0', 'r1'), ('r0', 'r2'), ('r1', 'r2'), ('r1', 's1'), ('r2', 's2'),
             ('s2', 's3'), ('s2','s4'), ('s3', 's4'),
             ('s1', 'h1'), ('s3', 'h2'), ('s3','h3'), ('s4', 'h4'), ('s4', 'h5')]
        )
        graph = DiagramGraph(config)
        tree = graph.getDiagramTree()
        fr = tree.freeNodes

        self.assertEqual(len(tree.routers), 3)
        self.assertEqual(len(tree.subnets), 2)

        if len(tree.subnets[0].switches) > 1: (bigSbntIdx, smallSbntIdx) = (0,1)
        else: (bigSbntIdx, smallSbntIdx) = (1,0)
           
        self.assertEqual(len(tree.subnets[smallSbntIdx].switches), 1)
        self.assertEqual(len(tree.subnets[smallSbntIdx].hosts), 1)
        self.assertEqual(len(tree.subnets[bigSbntIdx].switches), 3)
        self.assertEqual(len(tree.subnets[bigSbntIdx].hosts), 4)
        self.assertEqual(len(fr['routers']) + len(fr['switches']) + len(fr['hosts']), 0)
        self.assertEqual(len(tree.primaryLinks), 11)
        self.assertEqual(len(tree.secondaryLinks), 2)
        self.assertEqual(len(tree.redundantLinks), 26)
        self.assertEqual(len(tree.unusedLinks), 0)
