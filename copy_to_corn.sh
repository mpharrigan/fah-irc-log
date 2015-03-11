#!/bin/bash

# Get the right python env
source $HOME/.bashrc
export LANG=en_US.UTF-8

# change to directory of script
cd "$(dirname "$0")"

# Render html
python parse_log.py

# Special authentication script:
source authenticate.sh

# Copy
scp log.css out/* corn:~/WWW/fah/ >> scp.log
