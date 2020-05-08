# Getting Started

If you're new to Toynet, please reach out to [Tay](https://www.linkedin.com/in/takakonishimura/) or [Enmanuel](https://www.linkedin.com/in/edelanuez/) to be your onboarding buddy! :)

## Technical Requirements

#### Setup AWS

* Your onboarding buddy should assign you a new IAM User name with a temporary password. Visit https://909056806605.signin.aws.amazon.com/console to create new AWS password for yourself.

<span>
<kbd> <img src="/images/onboarding_sshingress.png" height=250 width=400/> </kbd>
<kbd> <img src="/images/onboarding_sshsecgrp.png" height=250 width=450/> </kbd>
</span>
<br/><br/>

* Add your home IP address to security group of your instance on `TCP Port 22`
* Grab the host identifier you need to run your EC2 instance by right clicking your instance in the console and selecting `Connect`

#### Setup SSH

<span>
<kbd> <img src="/images/onboarding_sshkeys.png" height=160 width=330/> </kbd>
<kbd> <img src="/images/onboarding_sshconfig.png" height=160 width=370/> </kbd>
</span>
<br/><br/>

* [Install VSCode](https://code.visualstudio.com/download) with the *Remote SSH Extension*
* [set up SSH](https://medium.com/@christyjacob4/using-vscode-remotely-on-an-ec2-instance-7822c4032cff) configurations for the instance asisgned to you
    
## Running ToyNet

You should already be able to run Toynet without any installations. Simply go to the `project-reclass/toynet/` directory and execute `./run_toynet.sh`. Toynet should output an image for you which you can checkout in the file directory on the left.

<span>
<kbd> <img src="/images/onboarding_run.png" height=200 width=400/> </kbd>
<kbd> <img src="/images/onboarding_openfolder.png" height=200 width=360/> </kbd>
</span>
<br/><br/>

If you want to ensure the image was successfully generated on subsequent runs, be sure to delete the previous image or add that step to the clean_toynet.py script.

<kbd> <img src="/images/onboarding_showpng.png" height=200 width=400/> </kbd>
<br/><br/>

# Codebase Structure

Outside of the scripts to run_toynet, the two most important directories to our current development are:

#### `project-reclass/toynet/toydiagram/`

Converts mingrammer's [Diagrams](https://diagrams.mingrammer.com) which are written for cloud infrastructure diagrams into network diagram nodes
* `network.py` - wraps `Node`, `Cluster`, and `Diagram` classes in `ToyNetNode`, `ToySubnet`, `ToyNetDiagram` respectively
* `diagramtree.py` - takes the network graph defined by mininet, and traverses it intelligently to deduce subnets and generate a tree structure to print
    
#### `project-reclass/toynet/toytopo/`

* `toytopo.py` - defines the network topology to visualize using Mininet's API
* `toynet.py` - a wrapper around a Mininet instance which can (1) translate the current network state visualization (PNG file) using ToyDiagrams, and expose an interactive GUI to the shell to change configurations or run queries

In the long run, we will be bringing up ToyNet instances inside a Django service. We will take a JSON-formatted configuration file from our React application which can be ingested into a `ToyTopo`(logy), and the resulting image will be returned to the front-end. Subsequent commands will allow the user to interact with the live network.

# Algorithms

If you're interested in algorithms, definintely checkout `diagramtree.py`.

1) We do a depth first traversal of a graph of nodes, where we first find the limits of the router graph by probing to the next node for switches. These routers on the edge are identified as gateway routers.
2) We then take each 'root' switch connected to a gateway router and do another depth first search to find the links of the subnetwork.

#### Unaddressed Issues:

Currently, we drop links (edges) between nodes which result in a cycle, but in the future we should distinguish which of these edges are valid (for example, multiple paths to the smae destination amongst routers), and which will cause issues (for example, a broadcast storm amongst switches).

We must also notify the user of nodes and links which were disregarded in the visualization. Alternatively, we can handle the issue of invalid configurations on the front end to save the servers and user time, but that requires validations in two places (React frontend and Django backend) which must be handled with care.
