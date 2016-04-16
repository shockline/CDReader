#!/bin/sh
if [ ! -f "pid" ]
then
    nohup python sup.py &
    echo $! > pid
fi
