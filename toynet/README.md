# Requirements

#### As a minimum viable product, ToyNet must be able to:
* Define a basic network configuration of routers, switches, & hosts (no modern devices like switch-routers)
* Visualize the defined network configuration
* Demonstrate responses to simple unix commandline interactions made to a specified host (including communicating with other hosts within this network)
* Run in an enviornment without access to internet (prison)

#### Some bonus features include:
* Protect the user from typos or invalid configurations
* Use the exact syntax of a real unix system (`host1> ping host2` instead of `mininet> host1 ping host2`)
* Run on the public internet with multiple users simultaneously
* Handle multiple users without a noticable delay
* Host accounts and memory of past configurations by user

# ToyNet System Design

## MVP

My initial design for this system is very simple. It will be a full-stack web application running on an Ubuntu enviornment, mostl likely on a virtual machine since most of our instructors will have a Mac or Windows machine.

#### Backend Technologies

After exploring neat and creative repositories and recieving some recommendations from friends, I identified two pre-existing projects to help me accomplish these requirements.

* [Mininet](https://github.com/mininet/mininet) emulates a complete network of hosts, links, and switches on a single machine. Stanford researchers Bob Lanz and Brandon Heller initially implemented Mininet to [research](https://github.com/mininet/mininet/wiki/Publications) Software Defined Networks (SDNs).
* [Diagrams](https://diagrams.mingrammer.com) neatly organizes and stylizes cloud architecture diagrams. Implimented by MinJae Kwon, Diagrams is now GitPitch is a markdown presentation service for developers. Diagrams is now integrated as [Cloud Diagram Widget](https://gitpitch.com/docs/diagram-features/cloud-diagrams/) of [GitPitch](https://gitpitch.com/).

<img src="/images/toynet_architecture.png" />


A React front-end with 3 components (visualization, interface for spawning the mininet, and a direct console to interact with the mininet) will connect to a stateful Django backend server which creates an intermediary object from the Mininet state to feed into Diagrams. This intermediate state will run some  algorithms

The backend Django server will handle interactions with configuration at a time, and kill the current mininet instnace to process an incoming "create" request.

## Thoughts for Bonus Features:

1. We must note that if we have multiple concurrent users as in a web application setup, destroying the current mininet session to spawn a new session would result in terminating one user's session early to service another user.
2. We can enable parallel processing either through a worker queue or spawning new processes, and this will likely be a challenge as mininet isn't designed to be used in a distributed environment.
3. To enable users to create an account and interact with it and save their past network designs, we must store each configuration they create in a database, most likely an RDS.

# Basic Wireframes

[Higher Fidelity Wireframes](https://docs.google.com/presentation/d/1qBIG4n3aiZ1wWQHOhJnE9b4o7gJcFZxrZSS6WbfhKyI/edit#slide=id.g71e07b3188_0_3115)

## Phase 0: Proof of Concept
<span><img src="/images/wireframe_mvp.png" height="250" width="400"/></span>

## Phase 1: Text-based Network Builder
<span>
<img src="/images/wireframe_text_config.png" height="250" width="400"/>
<img src="/images/wireframe_text_console.png" height="250" width="400"/>
</span>

## Phase 2: Modify Network Builder to be GUI-based
<span>
<img src="/images/wireframe_gui_config.png" height="250" width="400"/>
<img src="/images/wireframe_gui_link.png" height="250" width="400"/>
<img src="/images/wireframe_gui_launched.png" height="250" width="400"/>
</span>

## Phase 3: Modify Console Tab to be Host-Specific
<span>
<img src="/images/wireframe_cli_ping.png" height="250" width="400"/>
<img src="/images/wireframe_cli_arp.png" height="250" width="400"/>
</span>

## Phase 4: Add History Tab
<span>
<img src="/images/wireframe_cli_history.png" height="250" width="400"/>
</span>

