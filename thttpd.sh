#!/bin/bash
#Example script for spawning PyWW via thttpd server.
#See the thttpd man page.

INDEX="index.cgi"
PORT="8182"
DIR=`pwd`
WILD="**index.cgi"
USER="nobody"
HOST="localhost"
LOG=`pwd`/"pyww.log"
PID=`pwd`/"pyww.pid"
CSET="UTF-8"

thttpd -p $PORT -d $DIR -dd $DIR -c $WILD -h $HOST -l $LOG -i $PID -T $CSET $*

