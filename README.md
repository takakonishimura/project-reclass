# Project RECLASS

Project RECLASS is a not-for-profit vocational program focused on teaching computer networking to incarcerated veterans. 

Prisons hand-select students for their discipline and likelihood to pass the Network+ certification exam. The classes facilitate open-ended discussion, whether they be sharing expertise from past experiences or asking for more clarification on the subject.

We also develop hands-on labs, including a visual network simulation tool to demonstrate Linux command-line troubleshooting tools such as `arp` or `ip addr`! This repository is a central location for that software as well as some learning modules!

Learn more by [visiting our website](https://www.reclassltd.com)!

# ToyNet

[Official Design Document](https://github.com/takakonishimura/project-reclass/blob/master/toynet/README.md)

Most of our students do not have access to internet during or between classes, and many have never had hands-on experience with networks. This makes learning the Network+ curriculum a challenge of the imagination.

What if we could run an internet simulation on a single host which can run basic system administrator capabilities on a variety of emulated devices? We can run that simulation in a virtual machine and interact with it through a local instance of the web applicaiton.

ToyNet combines the network emulation capabilities of [mininet](https://github.com/mininet/mininet) with the visualization capabilities borrowed from [mingrammer's diagrams](https://github.com/mingrammer/diagrams) which was originaly built for system architecture diagrams of cloud infrastructure! For now we are just adding new hardware entities and using the "Cluster" feature for subnets. The technology stack is React front-end hooked up to a Django backend.

Checkout [some wireframe designs](https://docs.google.com/presentation/d/1qBIG4n3aiZ1wWQHOhJnE9b4o7gJcFZxrZSS6WbfhKyI/edit?usp=sharing) of the finished product!

# Other Projects Up for Grabs

Check out other [project ideas](https://docs.google.com/presentation/d/1HbHX3fKuG7k29GI0qZmr_EwTkXLa7rXTcQkzSnAAVvM/edit?usp=sharing) we have.
Reach out to [Tay](https://www.linkedin.com/in/takakonishimura/) if you want to contribute!

# Curriculum
### Lesson 1

* [Motivation](https://docs.google.com/presentation/d/1nPn9-x084IkWfUkYTADpa7UBuvugRWMr0vZFDOvDxSE/edit?usp=sharing)
* [OSI Model - Layer 1](https://docs.google.com/presentation/d/1kW0q9nSdCVy13571qeL9lkHH2Kh7uUr3mG4sjzSLHNM/edit?usp=sharing)
* [OSI Model - Layer 2](https://docs.google.com/presentation/d/158IbM7JtfA8nysjwBKO1LGaoWJnFE9U7V0h2oMHBn5s/edit?usp=sharing)
* [OSI Model - Layer 3](https://docs.google.com/presentation/d/1q0lIWJ30Is69ZYEHO2EpVDYBfyJX9ZU5vUkmtVMPBco/edit?usp=sharing)
* [OSI Model - Layer 4](https://docs.google.com/presentation/d/1OJms8_PDfjXeioJWyKMsEXlM-F2tYXNLWB7zg6r7u3c/edit?usp=sharing)
* [OSI Model - Layers 5-7](https://docs.google.com/presentation/d/1YTSIraYt5Md32wzwyfd9sdlo3a6dnA_XC98egMnsWyY/edit?usp=sharing)
* [Topologies](https://docs.google.com/presentation/d/1DlQ4Yp_JVCewlopG2UI4_tlp29diwfzPTUKRMmyhXEY/edit?usp=sharing)
* [Ethernet](https://docs.google.com/presentation/d/1GzojYw-sG3E9R6csR61zESMA26fJFK_3FasYG-Ok7_o/edit)

### Lesson 2

* [CIDR & ARP](https://docs.google.com/presentation/d/1FdFrl565odk45nBlvgMh3zVLkWaSMrjy-wsZpgBb0hw/edit)
* [ICMP](https://docs.google.com/presentation/d/1mio4J6XV2vNstiRLByvIS_viKaDUgCO6HKCNDNlwIWU/edit)
