class DiagramTree():
  "Deduce subnet groups from the list of routers & list of linked devices"
  
  graph = dict()
  knownDevices = set()

  def __init__(self, nodes={ 'routers': list(), 'switches': list(), 'links': list() }):

    if len(nodes['routers']): self.addAllNodes(nodes['routers'])
    else: self.addAllNodes(nodes['switches'])

    if len(nodes['links']): self.addAllLinks(nodes['links']) # prevent infinite loop
    print (self.graph)
  
  def addAllNodes(self, nodes):
    for n in nodes:
      self.graph[n] = dict()
      self.markKnown(n) # TODO @taytay: test mult routers

  def addAllLinks(self, links):
    while len(links):
      skippedLinks = list()
      for (n1, n2) in links:
        skipped = self.addLink(n1, n2)
        if skipped: skippedLinks.append(skipped)
      links = skippedLinks

  def addLink(self, n1, n2):
    print('adding links: ' + n1 + ' ' + n2)

    if not self.isKnown(n1) and not self.isKnown(n2):
      return (n1, n2)
    elif self.isKnown(n1) and not self.isKnown(n2):
      n1_parent = self.findParentNode(n1)
      n1_parent[n1][n2] = dict()
      self.markKnown(n2)
    elif not self.isKnown(n1) and self.isKnown(n2):
      n2_parent = self.findParentNode(n2)
      n2_parent[n2][n1] = dict()
      self.markKnown(n1)
    else:
      n1_parent = self.findParentNode(n1)
      n2_parent = self.findParentNode(n2)

      # routers should be closer to root
      if self.isRouter(n2):
        n2_parent[n2][n1] = n1_parent[n1]
        del n1_parent[n1]
      else:
        n1_parent[n1][n2] = n2_parent[n2]
        del n2_parent[n2]

  def findParentNode(self, name):
    return self.findParentNodeInSubtree(self.graph, name)
  
  def findParentNodeInSubtree(self, subtree, name):
    if not len(subtree.keys()):
      return None
    if name in subtree.keys():
      return subtree
    for node in subtree.keys():
      result = self.findParentNodeInSubtree(subtree[node], name)
      if result: return result
    return None

  def isKnown(self, name): return name in self.knownDevices
  def markKnown(self, device): self.knownDevices.add(device)

  def isRouter(self, name): return name.startswith('r')

  def isSwitch(self, name): return name.startswith('s')

  def isHost(self, name): return name.startswith('h')

  def getAllSubnets(self):
      subnets = list()
      return self.getSubnets(self.graph, subnets)

  def getSubnets(self, node, subnets):
      for child in node:
          if self.isRouter(child):
              self.getSubnets(node[child], subnets)
          else:
              devices = self.getDevicesInSubnet(node[child], child)
              subnets.append(devices)
      return subnets

  def getDevicesInSubnet(self, node, name):
      devices = [name]
      for child in node:
          devices += self.getDevicesInSubnet(node[child], child)
      return devices

  def getRouterList(self): return self.routers