import sys
from toynet.toynet import ToyNet

def run(filepath:str, visualize:bool=True, interact:bool=False, title:str='Toy Network'):
    """Takes an XML file and either visualizes or interacts with a network simulation
        depending on the flags passed in.
        Both use the ToyNet object's ToyTopoConfig as input.
        run script currently defaults to visualization but no iteraction if no flags set.
    """
    toynet = ToyNet(filepath)
    if visualize:
        print('TOYNET LOG---- creating new image representation')
        imageFileName = toynet.visualize(title)
        print('TOYNET LOG---- image created, see: ' + imageFileName)
    if interact:
        print('TOYNET LOG---- creating interactive simluation')
        toynet.interact()
        print('TOYNET LOG---- closing simulation')

if __name__ == '__main__':
    filepath = sys.argv[1]
    visualize = sys.argv[2].upper() == "TRUE"
    interact = sys.argv[3].upper() == "TRUE"

    run(filepath, visualize, interact)
