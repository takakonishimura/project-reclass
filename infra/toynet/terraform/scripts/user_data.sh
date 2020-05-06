#!/bin/bash
su - ubuntu -c "\
git clone https://github.com/takakonishimura/project-reclass.git && \
cd project-reclass/toynet/ && \
git submodule init && \
git submodule update && \
mininet/util/install.sh -s mininet -nfv"
