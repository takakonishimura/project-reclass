from diagrams import Cluster, Diagram, Node
from pathlib import Path
import os

class ToySubnet(Cluster):
  "Mingrammer's Cluster object repurposed for network diagrams"


class ToyNetDiagram(Diagram):
  "Mingrammer's Diagram object repurposed for network diagrams"


class ToyNetNode(Node):
  "Mingrammer's Node object repurposed for network diagrams"

  #TODO: TAYTAY is this hacky?
  def _load_icon(self):
    basedir = Path(os.path.abspath(os.path.dirname(__file__)) + "/taydiagram" )
    return os.path.join(basedir.parent, self._icon_dir, self._icon)
