from enum import Enum

class DeviceType(Enum):
    UNKNOWN= -1
    ROUTER = 0
    SWITCH = 1
    HOST = 2

class DiagramNode():
    def __init__(self, deviceName):
        self.deviceName = deviceName
        self.neighbors = set()
        self.deviceType = DeviceType.UNKNOWN

        if deviceName.startswith('r'): self.deviceType = DeviceType.ROUTER
        elif deviceName.startswith('s'): self.deviceType = DeviceType.SWITCH
        elif deviceName.startswith('h'): self.deviceType = DeviceType.HOST

class DiagramSubnet():
    def __init__(self, rootSwitch):
        self.switches = [rootSwitch.deviceName]
        self.hosts = list()
        self.links = list()
        self.visited = set()

        (self.links, descendantSwitches, self.hosts) = self.traverseSubnet(rootSwitch)
        self.switches.extend(descendantSwitches)

    # Traversing Graphs to form Tree
    def traverseSubnet(self, rootSwitch):
        return self.findSwitchLinksAndHosts(rootSwitch)

    def findSwitchLinksAndHosts(self, node):
        # for processing
        switchNeighbors = list()

        # for output
        subnetLinks = list()
        subnetSwitches = list()
        subnetHosts = list()

        # operate
        self.visited.add(node.deviceName)

        for neighbor in node.neighbors:
            if neighbor.deviceName in self.visited:
                print('__INFO___ skipping already visited device ' + neighbor.deviceName)
            else:
                if neighbor.deviceType == DeviceType.SWITCH:
                    switchNeighbors.append(neighbor)

                    subnetSwitches.append(neighbor.deviceName)
                    subnetLinks.append((node.deviceName, neighbor.deviceName))
                elif neighbor.deviceType == DeviceType.HOST:
                    switchNeighbors.append(neighbor)

                    subnetHosts.append(neighbor.deviceName)
                    subnetLinks.append((node.deviceName, neighbor.deviceName))
                elif neighbor.deviceType == DeviceType.ROUTER:
                    print('__INFO___ skipping router ' + neighbor.deviceName + ' while processing ' + node.deviceName + ' for subnets')
                else:
                    print('__ERROR__ device is not a router, switch, or host so subnet will not process it')

        # basecase
        if not len(switchNeighbors): return (subnetLinks, subnetSwitches, subnetHosts)

        # recursion + aggregation
        for switchNeighbor in switchNeighbors:
            descendants = self.findSwitchLinksAndHosts(switchNeighbor)
            subnetLinks.extend(descendants[0])
            subnetSwitches.extend(descendants[1])
            subnetHosts.extend(descendants[2])

        return (subnetLinks, subnetSwitches, subnetHosts)

class DiagramTree():
    "Deduce subnet groups from the list of routers & list of linked devices"

    def __init__(self, devices={ 'routers': list(), 'switches': list(), 'hosts': list(), 'links': list() }):
        # for processing
        self.nodeLookup = dict() # only for intermediary calculations
        self.visited = set()

        # for output
        self.routers = devices['routers']
        self.links = list()
        self.subnets = list()

        if len(devices['routers']) > 0: 
            routerName = devices['routers'][0]

            self.addAllDevicesToGraph(devices['routers'] + devices['switches'] + devices['hosts'])
            self.addAllLinksToGraph(devices['links'])

            (self.links, subnetRoots) =  self.traverseRouters(self.nodeLookup[routerName])
            for subnetRoot in subnetRoots:
                self.subnets.append(DiagramSubnet(subnetRoot))

        elif len(devices['switches']) > 0:
            #TODO: TAYTAY infinite loop?
            switchName = devices['routers'][0]

            self.addAllDevicesToGraph(devices['switches'] + devices['hosts'])
            self.addAllLinksToGraph(devices['links'])

            self.subnets = [DiagramSubnet(self.nodeLookup[switchName])]
        else:
            print('__ERROR___ does not have root, there is no defined network')
            self.addAllDevicesToGraph(devices['switches'] + devices['hosts'])

    # Setup Building Graph to Traverse
    def addAllDevicesToGraph(self, devices):
        for deviceName in devices:
            self.nodeLookup[deviceName] = DiagramNode(deviceName)

    def addAllLinksToGraph(self, links):
        for (d1, d2) in links:
            self.nodeLookup[d1].neighbors.add(self.nodeLookup[d2])
            self.nodeLookup[d2].neighbors.add(self.nodeLookup[d1])

    # Traversing Graphs to form Tree
    def traverseRouters(self, rootRouter):
        return self.findRouterLinksAndSubnets(rootRouter)

    def findRouterLinksAndSubnets(self, node):
        # for processing
        routerNeighbors = list()

        # to aggregate
        routerLinks = list()
        subnetNeighbors = list()

        # operate
        self.visited.add(node.deviceName)

        for neighbor in node.neighbors:
            if neighbor.deviceName in self.visited:
                print('__INFO___ skipping already visited device ' + neighbor.deviceName)
            else:
                if neighbor.deviceType == DeviceType.ROUTER:
                    routerNeighbors.append(neighbor)
                    routerLinks.append((node.deviceName, neighbor.deviceName))
                elif neighbor.deviceType == DeviceType.SWITCH:
                    subnetNeighbors.append(neighbor)
                    routerLinks.append((node.deviceName, neighbor.deviceName))
                else:
                    print('__ERROR__ a device is connected to a router that is netiher a router nor a switch')

        # basecase
        if not len(routerNeighbors): return (routerLinks, subnetNeighbors)

        # recurse & aggregate
        for routerNeighbor in routerNeighbors:
            (descendantLinks, descendentSubnets) = self.findRouterLinksAndSubnets(routerNeighbor)
            routerLinks.extend(descendantLinks)
            subnetNeighbors.extend(descendentSubnets)

        return (routerLinks, subnetNeighbors)
