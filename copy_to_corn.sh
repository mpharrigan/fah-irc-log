#!/bin/bash

# Get the right python env
source $HOME/.bashrc

# change to directory of script
cd "$(dirname "$0")"

# Render html
./parse_log.py

# Special authentication script:
source authenticate.sh

# Copy
scp log.css log.html log.content.html about.html corn:~/WWW/fah/ >> scp.log
