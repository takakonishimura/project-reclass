from typing import Set, Dict, List, Tuple, Any
import functools

from toydiagram.diagramEntity import DiagramEntity, DeviceType

from util.error import DiagramGraphError
import util.typecheck as tc

class Name(str): pass


class DiagramNode(DiagramEntity):
    """A DiagramNode represents a host, switch, or router in a Mininet.
        It connects neighbors in a graph which is traversed to create the DiagramTree.

    Raises:
        DiagramGraphError

    Attributes:
        deviceName:     str -- name of host, switch, or router
        neighbors:      Set[DiagramNode] -- DiagramNodes connected to this DiagramNode
        deviceType:     DeviceType -- type host, switch, or router
    """
    def __init__(self, device: Name):
        tc.inputTypeCheck(device, 'device', str)

        self.deviceName: Name = device
        self.neighbors: Set[DiagramNode] = set()

        if device.startswith('r'): self.deviceType: DeviceType = DeviceType.ROUTER
        elif device.startswith('s'): self.deviceType: DeviceType = DeviceType.SWITCH
        elif device.startswith('h'): self.deviceType: DeviceType = DeviceType.HOST
        else:
            errorMsg = 'Device name "' + self.deviceName + '" cannot be mapped to a device type'
            raise DiagramGraphError(errorMsg)

    def __addNeighbor(self, nbr: 'DiagramNode') -> None:
        if (nbr in self.neighbors): return

        # add to each other
        self.neighbors.add(nbr)
        nbr.__addNeighbor(self)

    def addNeighbor(self, nbr: 'DiagramNode') -> None:
        tc.inputTypeCheck(nbr, 'nbr', DiagramNode)

        if self.isHost() and len(self.neighbors) == 1:
            raise DiagramGraphError('Device type HOST cannot have second neighbor ' + nbr.deviceName, self)
        if nbr.isHost() and len(nbr.neighbors) == 1:
            raise DiagramGraphError('Device type HOST cannot have second neighbor ' + self.deviceName, self)

        if self.isHost() and not nbr.isSwitch():
            raise DiagramGraphError('Device type HOST cannot be neighbors with ' + nbr.deviceType.name, self)
        if nbr.isHost() and not self.isSwitch():
            raise DiagramGraphError('Device type ' + self.deviceType.name + ' cannot be neighbors with HOST', self)

        if self.isRouter() and not nbr.isSwitch() and not nbr.isRouter():
            raise DiagramGraphError('Device type ROUTER cannot be neighbors with ' + nbr.deviceType.name, self)
        if not self.isSwitch() and not self.isRouter() and nbr.isRouter():
            raise DiagramGraphError('Device type ' + self.deviceType.name + ' cannot be neighbors with ROUTER', self)

        self.__addNeighbor(nbr)

    def isRouter(self) -> bool: return self.deviceType == DeviceType.ROUTER
    def isSwitch(self) -> bool: return self.deviceType == DeviceType.SWITCH
    def isHost(self) -> bool: return self.deviceType == DeviceType.HOST    

    def toString(self) -> str:
        nbrs: str = ''
        if len(self.neighbors) > 0:
            neighborNames = map(lambda neighbor: neighbor.deviceName, self.neighbors)
            nbrs = functools.reduce(lambda names,nm: (names + ',' + nm),  neighborNames)
        description: str = '{ type: ' + self.deviceType.name + ' | neighbors: [' + nbrs + '] }'
        return self.deviceName + ' = ' + description

    def toShortString(self) -> str:
        description = '[' + self.deviceType.name + ', ' + str(len(self.neighbors)) + ' neighbors]'
        return self.deviceName + ' ' + description


class DiagramSubnet(DiagramEntity):
    """DiagramSubnet is a tree structure of "primaryLinks" from traversing DiagramGraph.
        The root of DiagramSubnets are switches attached to routers. DiagramSubnet also
        records "secondaryLinks" which are links to nodes already accounted for. This
        traversal builds a natural-looking network exactly as the end user intended it.

    Raises:
        DiagramGraphError
    
    Attributes:
        switches:       List[Name] -- switches connected to and including root Switch
        hosts:          List[Name] -- hosts connected to these switches
    """            

    def __init__(self):
        self.switches: List[Name] = list()
        self.hosts: List[Name] = list()

    def addSwitch(self, switch: Name) -> None: self.switches.append(switch)
    def addHost(self, host: Name) -> None: self.hosts.append(host)

    def toString(self) -> str:
        switches: str = functools.reduce(lambda swts,s: swts+','+s, self.switches)
        hosts: str = functools.reduce(lambda hsts,h: hsts+','+h, self.hosts)
        return 'Subnet: { switches: [' + switches + '] | hosts: [' + hosts + ']}'

    def toShortString(self) -> str:
        return '[' + str(len(self.switches)) + ' switches, ' + str(len(hosts)) + ' hosts]'


class DiagramTree(DiagramEntity):
    """DiagramTree is a tree structure of "primaryLinks" which traversing DiagramGraph.
        DiagramTree also records "secondaryLinks" which are links to nodes already
        accounted for. This traversal builds a natural-looking network exactly as the
        end user intended it.

    Raises:
        DiagramGraphError
    
    Attributes:
        routers:        List[Name] -- routers connected to and including root Router
        subnets:        List[Subnet] -- subnets connected to a router from root Switch
        freeNodes:      Dict[str,List[Name]] -- connections between nodes picked up 
                            during tree traversals
        visited:        Set[Name] -- names of devices already traversed

        primaryLinks:   List[Tuple[Name,Name]] -- connections between nodes picked up 
                            during tree traversals
        secondaryLinks: List[Tuple[Name,Name]] -- connections between nodes where one 
                            node has already been visited
        redundantLinks: Set[Tuple[Name,Name]] -- set of connections between nodes which
                            should not be added because its matching reverse Pair is
                            already added
        unusedLinks:    Set[Tuple[Name,Name]] -- set of connections between nodes which
                            were not included in the Tree construction
    """

    def __init__(self):
        self.routers: List[Name] = list()
        self.subnets: List[DiagramSubnet] = list()
        self.freeNodes: Dict[str,List[Name]] = {
            'routers': list(),
            'switches': list(),
            'hosts': list()
        }
        self.visited: Set[Name] = set()

        self.primaryLinks: List[Tuple[Name,Name]] = list()
        self.secondaryLinks: List[Tuple[Name,Name]] = list()
        self.redundantLinks: Set[Tupe[Name,Name]] = set()
        self.unusedLinks: Set[Tupe[Name,Name]] = list()

    def addFreeNode(self, node: DiagramNode) -> None:
        if node.isRouter():
            self.freeNodes['routers'].append(node.deviceName)
        elif node.isSwitch():
            self.freeNodes['switches'].append(node.deviceName)
        elif node.isHost():
            self.freeNodes['hosts'].append(node.deviceName)
        else:
            raise DiagramGraphError('Device type ' + node.deviceType.name + ' not recognized for ' + node.deviceName, self)

    def addRouter(self, router: Name) -> None: self.routers.append(router)
    def addSubnet(self, subnet: DiagramSubnet) -> None: self.subnets.append(subnet)

    def addPrimaryLink(self, nm1: str, nm2: str) -> None:
        self.primaryLinks.append((nm1, nm2))
        self.redundantLinks.add((nm1, nm2))
        self.redundantLinks.add((nm2, nm1))

    def addSecondaryLink(self, nm1: str, nm2: str) -> None:
        self.secondaryLinks.append((nm1, nm2))
        self.redundantLinks.add((nm1, nm2))
        self.redundantLinks.add((nm2, nm1))

    def isRedundantLink(self, nm1: str, nm2: str) -> bool: return (nm1,nm2) in self.redundantLinks
    def addUnusedLink(self, nm1: str, nm2: str) -> None: self.unusedLinks.append((nm1, nm2))

    def toString(self) -> str:
        routers: str = '[' + functools.reduce(lambda rtrs,r: rtrs+','+r, self.routers) + ']'
        subnets: str = '[' + functools.reduce(lambda sbnts,s: sbnts+','+s, map(lambda sbnt: sbnt.toShortString(), self.subnets)) + ']'

        fr = self.free
        free: str = '{ rtrs:' + str(len(fr['routers'])) + ',swts:' + str(len(fr['switches'])) + ',hosts:'+ str(len(fr['hosts'])) + ' }'
        lnks: str = '{ prmry:' + len(self.primaryLinks) + ',scndry:' + len(self.secondaryLinks) + ' }'
        return 'Tree: { rtrs: ' + routers + ' | sbnts: ' + subnets + ' | free: ' + free + ' | links: ' + lnks + '}'

    def toShortString(self) -> str:
        rtrs = str(len(self.routers))
        free = str(len(self.free['routers']) + len(self.free['switches']) + len(self.free['hosts']))
        links = str(len(self.primaryLinks) + len(self.secondaryLinks))
        sbnts = str(len(self.subnets))
        return '[' + rtrs + ' routers, ' + free + ' free nodes, ' + links + ' links, ' + sbnts + ' subnets]'


class DiagramGraph(DiagramEntity):
    """A DiagramGraph represents the end user's configuration of a network topology.
        It takes as input a list of router, switche, and host names as well as links
        between them. DiagramGraph instantiates a DiagramNode for each of these entities
        and applies the links as "neighbors" in the respective nodes.

        DiagramGraphs can be traversed depth-first from a particular router to produce
        a DiagramTree which can be visualized for the end user.

    Raises:
        DiagramGraphError

    Attributes:
        devices:    Dict[str,DiagramNode] -- mapping of device names to DiagramNode objects
        root:       DiagramNode -- name of root device (either user specified or deduced by class)
        links:      List[Tuple[Name,Name]] -- stored from input to check for unused links in Tree
    """

    def __init__(self, devices: Dict[Name,List[Any]], root: Name=None):
        """Input parameter "devices" takes following structure:
            {
                'routers': ['r0', 'r1'],
                'switches': ['s1'],
                'hosts': ['h1', 'h2'],
                'links': [ ('r0','r1'), ('r1', 's1'), ('s1', 'h1'), ('s1', 'h2') ]
            }
            Input parameter "root" is an optional parameter which attempts to
            preserve the user's intended tree structure (for example, we might use
            the first node they defined, or allow them to select the node they wish
            to traverse from explicitly).
        """
        tc.inputTypeCheck(devices, 'devices', dict)
        if 'routers' not in devices: raise DiagramGraphError('DiagramGraph input missing \'routers\'')
        if 'switches' not in devices: raise DiagramGraphError('DiagramGraph input missing \'switches\'')
        if 'hosts' not in devices: raise DiagramGraphError('DiagramGraph input missing \'hosts\'')
        if 'links' not in devices: raise DiagramGraphError('DiagramGraph input missing \'links\'')
        routers: List[Name] = devices['routers']
        switches: List[Name] = devices['switches']
        hosts: List[Name] = devices['hosts']
        self.links: List[Tuple[Name,Name]] = devices['links']

        self.devices: Dict[Name,DiagramNode] = dict()
        self.__addAllDevicesToGraph(routers + switches + hosts)
        self.__addAllLinksToGraph(self.links)

        if len(routers) > 0: 
            print('__INFO___ network selected router as root: ' + routers[0])
            self.root: DiagramNode = self.devices[routers[0]]
        elif len(switches) > 0:
            print('__WARN___ network has no routers; selected switch as root: ' + switches[0])
            self.root: DiagramNode = self.devices[switches[0]]
        elif len(hosts) > 0:
            print('__WARN___ network has no routers or switches' )
        else:
            raise DiagramGraphError('network is missing devices')

        if root is not None and hasattr(self.devices, root):
            print('__INFO___ network was provided root: ' + root)
            self.root: DiagramNode = self.devices[root]

    def __addAllDevicesToGraph(self, deviceList: List[str]) -> None:
        for name in deviceList: self.devices[name] = DiagramNode(name)

    def __addAllLinksToGraph(self, links: List[Tuple[str,str]]) -> None:
        for (nm1, nm2) in links: 
            if nm1 not in self.devices:
                raise DiagramGraphError('Device ' + nm1 + ' not found in Graph devices')                
            elif nm2 not in self.devices:
                raise DiagramGraphError('Device ' + nm2 + ' not found in Graph devices')
            else:
                self.devices[nm1].addNeighbor(self.devices[nm2])

    def getDiagramTree(self) -> DiagramTree:
        """Traverse DiagramGraph to deduce DiagramTree"""
        tree: DiagramTree = DiagramTree()

        # build connections
        if self.root:  
            if self.root.isRouter():
                tree = self.findRouterLinksAndSubnetRoots(tree, self.root)
            elif self.root.isSwitch():
                subnet = DiagramSubnet()
                (tree, _) = self.findSwithLinksAndHosts(tree, subnet, self.root)
                tree.addSubnet(subnet)
            else:
                raise DiagramGraphError('Root node must be type ROUTER or SWITCH', self)

        for dvcname, dvc in self.devices.items():
            if (dvcname not in tree.visited) or not tree.visited: tree.addFreeNode(dvc)

        for (dvc1, dvc2) in self.links:
            if ((dvc1, dvc2) not in tree.redundantLinks): tree.addUnusedLink(dvc1,dvc2)

        return tree

    def findRouterLinksAndSubnetRoots(self,
        tree: DiagramTree,
        router: DiagramNode,
        ) -> Tuple[DiagramTree,Set[Name]]:
        """Traverse through routers then attached Subnets to build DiagramTree"""

        tree.visited.add(router.deviceName)
        tree.addRouter(router.deviceName)

        for neighbor in router.neighbors:
            if neighbor.deviceName not in tree.visited:
                tree.addPrimaryLink(router.deviceName, neighbor.deviceName)

                if neighbor.isRouter():
                    tree = self.findRouterLinksAndSubnetRoots(tree, neighbor)
                elif neighbor.isSwitch():
                    subnet = DiagramSubnet()
                    (tree, subnet) = self.findSwitchLinksAndHosts(tree, subnet, neighbor)
                    tree.addSubnet(subnet)
                else:
                    raise DiagramGraphError('Device type ROUTER cannot be neighbors with ' + neighbor.deviceName, self)
            else:
                if not tree.isRedundantLink(router.deviceName, neighbor.deviceName):
                    tree.addSecondaryLink(router.deviceName, neighbor.deviceName)

        return tree

    def findSwitchLinksAndHosts(self,
            tree: DiagramTree,
            subnet: DiagramSubnet,
            switch: DiagramNode
        ) -> Tuple[DiagramTree, DiagramSubnet, Set[Name]]:
        """Traverse through switches to build DiagramSubnet"""

        # add switch
        tree.visited.add(switch.deviceName)
        subnet.addSwitch(switch.deviceName)  

        # operate on descendants
        for neighbor in switch.neighbors:
            if neighbor.deviceName not in tree.visited:
                tree.addPrimaryLink(switch.deviceName, neighbor.deviceName)

                if neighbor.isSwitch():
                    (tree, subnet) = self.findSwitchLinksAndHosts(tree, subnet, neighbor)
                elif neighbor.isHost():
                    # add host
                    tree.visited.add(neighbor.deviceName)
                    subnet.addHost(neighbor.deviceName)
                else:
                    raise DiagramGraphError('Device type SWITCH cannot be neighbors with ' + neighbor.deviceName, self)
            else:
                if not tree.isRedundantLink(neighbor.deviceName, switch.deviceName):
                    tree.addSecondaryLink(switch.deviceName, neighbor.deviceName)

        return (tree, subnet)

    def toString(self) -> str:
        dvcList: str = ''
        if len(self.deviceList.keys()) > 0:
            dvcDescs = map(lambda dvc: dvc.toShortString(), self.deviceList.keys())
            dvcList = functools.reduce(lambda list,desc: (list + ', ' + desc), dvcDescs)
        return 'Graph: { rootDevice: ' + self.root + ' | devices: [' + dvcList + ']}'

    def toShortString(self) -> str:
        return '[ root: ' + self.root + ', ' + str(len(self.devceList)) + 'devices ]'
