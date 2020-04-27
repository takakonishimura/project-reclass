from toynet.toynet import ToyNet
from toynet.toytopo import ToyTopo

def run():
    "Create Mininet & Visualize it"

    toynet = ToyNet(topology=ToyTopo()) # ToyNet( topo=TreeTopo( depth=2, fanout=6 ) )

    toynet.visualize()
    #toynet.interact()

if __name__== "__main__":
  run() 
