#!/usr/bin/env bash

FILEDIR="sample_inputs/"
FILENAME="sample.xml"
VISUALIZE="FALSE"
INTERACT="FALSE"

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -f|--filename)
    FILENAME="$2"
    shift # past argument
    shift # past value
    ;;
    -v|--visualize)
    VISUALIZE="TRUE"
    shift # past argument
    ;;
    -i|--interact)
    INTERACT="TRUE"
    shift # past argument
    ;;
esac
done

echo 'TOYNET LOG---- cleaning any previous runs'
sudo python3 clean_toynet.py

echo 'TOYNET LOG---- creating new toynet'

if [[ "FALSE" == "$VISUALIZE" ]] && [[ "FALSE" == "$INTERACT" ]];
then
    echo '__INFO___ Defaulting to just Visualization'
    VISUALIZE="TRUE"
    INTERACT="FALSE"
fi
sudo python3 create_and_visualize.py ${FILEDIR}${FILENAME} ${TITLE} ${VISUALIZE} ${INTERACT}

echo 'TOYNET LOG---- done processing'