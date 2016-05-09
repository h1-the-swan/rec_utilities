#!/bin/bash
set -e
E_NOARGS=75

if [ -z "$1" ]
    then
    echo "Usage: `basename $0` file.net"
    exit $E_NOARGS
fi


FROM=$(( $(grep -n "^\*edges" $1 | cut -f 1 -d :) + 1))
tail -n +$FROM $1
