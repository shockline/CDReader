#!/bin/bash
if [ ! -f "pid" ]
then
    curpath=$(cd `dirname $0`; pwd)
    nohup python MultiTraining.py &
    echo $! > pid
fi