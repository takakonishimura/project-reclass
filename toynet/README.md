# Introduction

Most of our students do not have access to internet during or between classes, and many have never had hands-on experience with networks. This makes learning the Network+ curriculum a challenge of the imagination.

What if we could run an internet simulation on a single host which can run basic system administrator capabilities on a variety of emulated devices? We can run that simulation in a virtual machine and interact with it through a local instance of the web applicaiton.

ToyNet combines the network emulation capabilities of [Mininet](https://github.com/mininet/mininet) with the visualization capabilities of mingrammer's [Diagrams](https://github.com/mingrammer/diagrams), which was originaly built for system architecture diagrams of cloud infrastructure! For now we are just adding new hardware entities and using the "Cluster" feature for subnets. The technology stack consists of a React frontend hooked up to a Django backend.

Here are [some wireframe designs](https://docs.google.com/presentation/d/1qBIG4n3aiZ1wWQHOhJnE9b4o7gJcFZxrZSS6WbfhKyI/edit?usp=sharing) of different phases of the product.

# Technical Requirements

#### As a minimum viable product, ToyNet must be able to:
* Define a basic network configuration with traditional devices such as routers, switches, and hosts 
* Visualize the defined network configuration
* Demonstrate responses to simple Linux commandline interactions made to specified hosts (includes communication with other hosts on the network)
* Run without internet access (for example: in a prison)

#### Some bonus features include:
* Protect the user from typos or invalid configurations
* Provide a fully featured interface to the Mininet CLI
* Handle multiple users without a noticable delay as a publicly-hosted web service for demonstration purposes
* Host accounts and record configurations per user to reinstantiate in the future

# ToyNet System Design

## MVP

My initial design for this system is very simple: a full-stack web application with a React frontend and Django backend running on Ubuntu. Since most of our instructors use a Mac or Windows machine, it will most likely run on a virtual machine.

### Leveraged Technologies

After exploring neat repositories and recieving some recommendations from others, I identified two pre-existing projects to help me accomplish these requirements:

* [Mininet](https://github.com/mininet/mininet) emulates a complete network of hosts, links, and switches on a single machine. Stanford researchers Bob Lanz and Brandon Heller initially implemented Mininet to [research](https://github.com/mininet/mininet/wiki/Publications) software defined networks.
* [Diagrams](https://diagrams.mingrammer.com) by MinJae Kwon neatly organizes and stylizes cloud architecture diagrams. It is now integrated as the [Cloud Diagram Widget](https://gitpitch.com/docs/diagram-features/cloud-diagrams/) of [GitPitch](https://gitpitch.com/), a markdown presentation service for developers.

<img src="/images/toynet_architecture.png" />

## Frontend

[React](https://reactjs.org) is a JavaScript library for building component-based user interfaces with declarative views. We have three basic components in ToyNet's MVP:
* network visualization (image)
* text interface to construct netowrk configurations
* text interface to interact directly with the Mininet instance

Each component contains a controller which manages state as well as JSX to describe how to render the state data. The controllers take user input and communicate with the backend on behalf of the component via pre-defined URL routes. They then update the application with the returned results.

These components communicate state to each other using [Redux](https://redux.js.org), a state container for JavaScript which centralizes an application's state and logic rather than dispersing that information in the separate components.

## Backend

[Django](https://www.djangoproject.com) is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. ToyNet's backend service takes a network configuration and returns a PNG image representing the current network as well as a session key. The session key is used by the frontend to indicate the Mininet instance within which to execute subsequent commands. In the first implementation, this stateful service handles one instance at a time; creating and launching a new network requires killing the currently running instance.

The following steps describe how the backend handles network creation and updates:
1. The service creates an intermediary representation from the Mininet state to feed into Diagrams.
2. This intermediate state computes subnets and runs some validations.
3. Diagrams generates a PNG file by translating the intermediate state into a series of commands in the Diagrams DSL.

## Thoughts for Bonus Features:

* In a web application setup, we cannot predict when and how many users will want to try this product, so we must support concurrent users.
* If past network designs are accessible, we must take proper precautions when a single user accesses the network from different devices or browser tabs.
* To enable users to create an account and save past network designs, we must store each configuration they create in a database.

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

