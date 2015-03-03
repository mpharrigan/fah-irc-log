#!/bin/bash

# change to directory of script
cd "$(dirname "$0")"

./parse_log.py
scp log.html log.content.html about.html corn:~/WWW/fah/ >> scp.log
