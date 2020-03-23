#!/bin/bash
cd toynet

echo 'TOYNET LOG---- cleaning any previous runs'
sudo python3 clean_toynet.py

echo 'TOYNET LOG---- creating new toynet'
sudo python3 create_and_visualize.py

echo 'TOYNET LOG---- done processing, see toy_network.png'
