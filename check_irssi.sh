#!/bin/bash

line=`screen -ls | grep irssi`
if [ $? -ne 0 ]
then
    screen -S irssi -d -m irssi
    echo "Restarted irssi"
fi
