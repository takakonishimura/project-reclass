import unittest

from toydiagram.diagramTree import DiagramNode, DeviceType
from util.error import DiagramGraphError, TypeCheckError

class TestDiagramNodeMethods(unittest.TestCase):

    def test_DiagramNode__basicCreation(self):
        host = DiagramNode('h1')
        switch = DiagramNode('s1')
        router = DiagramNode('r1')

        self.assertEqual(host.deviceName, 'h1')
        self.assertEqual(host.deviceType, DeviceType.HOST)
        self.assertEqual(len(host.neighbors), 0)

        self.assertEqual(switch.deviceName, 's1')
        self.assertEqual(switch.deviceType, DeviceType.SWITCH)
        self.assertEqual(len(switch.neighbors), 0)

        self.assertEqual(router.deviceName, 'r1')
        self.assertEqual(router.deviceType, DeviceType.ROUTER)
        self.assertEqual(len(router.neighbors), 0)

    def test_DiagramNode__badCreation(self):
        with self.assertRaises(DiagramGraphError) as cm:
            DiagramNode('not_hsr')

        self.assertEqual(cm.exception.message, 'Device name "not_hsr" cannot be mapped to a device type')

        with self.assertRaises(TypeCheckError) as cm:
            DiagramNode(1000)

        self.assertEqual(cm.exception.message, 'device should be <class \'str\'> but is: <class \'int\'>')
        self.assertEqual(cm.exception.input, 1000)

    def test_DiagramNode__addGoodNeighbors(self):
        r1 = DiagramNode('r1')
        r2 = DiagramNode('r2')
        s1 = DiagramNode('s1')
        s2 = DiagramNode('s2')
        h1 = DiagramNode('h1')
        h2 = DiagramNode('h2')

        r1.addNeighbor(r2)
        self.assertTrue(r2 in r1.neighbors)
        self.assertTrue(r1 in r2.neighbors)
        self.assertEqual(len(r1.neighbors), 1)
        self.assertEqual(len(r2.neighbors), 1)
    
        r1.addNeighbor(s1)
        self.assertTrue(s1 in r1.neighbors)
        self.assertTrue(r1 in s1.neighbors)
        self.assertEqual(len(r1.neighbors), 2)
        self.assertEqual(len(r2.neighbors), 1)
        self.assertEqual(len(s1.neighbors), 1)
        
        s1.addNeighbor(s2)
        self.assertTrue(s2 in s1.neighbors)
        self.assertTrue(s1 in s2.neighbors)
        self.assertEqual(len(r1.neighbors), 2)
        self.assertEqual(len(r2.neighbors), 1)
        self.assertEqual(len(s1.neighbors), 2)
        self.assertEqual(len(s2.neighbors), 1)

        s1.addNeighbor(h1)
        self.assertTrue(h1 in s1.neighbors)
        self.assertTrue(s1 in h1.neighbors)
        self.assertEqual(len(r1.neighbors), 2)
        self.assertEqual(len(r2.neighbors), 1)
        self.assertEqual(len(s1.neighbors), 3)
        self.assertEqual(len(s2.neighbors), 1)
        self.assertEqual(len(h1.neighbors), 1)

    def test_DiagramNode__addBadNeighbors(self):
        router = DiagramNode('routername')
        switch = DiagramNode('switchname')
        switch2 = DiagramNode('switchtwo')
        host = DiagramNode('hostname')
        host2 = DiagramNode('hosttwo')

        with self.assertRaises(DiagramGraphError) as cm:
            router.addNeighbor(host)
        self.assertEqual(cm.exception.message, 'Device type ROUTER cannot be neighbors with HOST (Entity: routername [ROUTER, 0 neighbors])')
        self.assertEqual(len(router.neighbors), 0)
        self.assertEqual(len(host.neighbors), 0)

        with self.assertRaises(DiagramGraphError) as cm:
            host.addNeighbor(router)
        self.assertEqual(cm.exception.message, 'Device type HOST cannot be neighbors with ROUTER (Entity: hostname [HOST, 0 neighbors])')
        self.assertEqual(len(router.neighbors), 0)
        self.assertEqual(len(host.neighbors), 0)

        with self.assertRaises(DiagramGraphError) as cm:
            host.addNeighbor(host2)
        self.assertEqual(cm.exception.message, 'Device type HOST cannot be neighbors with HOST (Entity: hostname [HOST, 0 neighbors])')
        self.assertEqual(len(router.neighbors), 0)
        self.assertEqual(len(host.neighbors), 0)

        host.addNeighbor(switch)
        self.assertEqual(len(host.neighbors), 1)

        with self.assertRaises(DiagramGraphError) as cm:
            host.addNeighbor(switch2)
        self.assertEqual(cm.exception.message, 'Device type HOST cannot have second neighbor switchtwo (Entity: hostname [HOST, 1 neighbors])')
        self.assertEqual(len(router.neighbors), 0)
        self.assertEqual(len(host.neighbors), 1)


    def test_DiagramNode__stringify(self):
        host = DiagramNode('hostname')
        switch = DiagramNode('switchname')
        router = DiagramNode('routername')

        self.assertEqual('hostname = { type: HOST | neighbors: [] }', host.toString())
        self.assertEqual('hostname [HOST, 0 neighbors]', host.toShortString())

        switch.addNeighbor(host)
        switch.addNeighbor(router)

        string = switch.toString()
        sw1 = 'switchname = { type: SWITCH | neighbors: '
        nbr = ['[routername,hostname]','[hostname,routername]']
        sw2 = ' }'
        
        self.assertTrue( string == (sw1 + nbr[0] + sw2) or string == (sw1 + nbr[1] + sw2) )
        self.assertEqual('switchname [SWITCH, 2 neighbors]', switch.toShortString())

    def test_DiagramNode__isNode(self):
        host = DiagramNode('hostname')
        switch = DiagramNode('switchname')
        router = DiagramNode('routername')

        self.assertTrue(router.isRouter())
        self.assertFalse(router.isSwitch())
        self.assertFalse(router.isHost())

        self.assertFalse(switch.isRouter())
        self.assertTrue(switch.isSwitch())
        self.assertFalse(switch.isHost())

        self.assertFalse(host.isRouter())
        self.assertFalse(host.isSwitch())
        self.assertTrue(host.isHost())