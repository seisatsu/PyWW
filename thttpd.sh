#!/bin/sh
#Example script for spawning PyWW via thttpd server.
#See the thttpd man page.

INDEX="index.cgi"
PORT="8182"
DIR=`pwd`
USER="nobody"
WILD="**index.cgi"
HOST="localhost"
LOG=`pwd`/"pyww.log"
PID=`pwd`/"pyww.pid"
CSET="UTF-8"

thttpd -p $PORT -d $DIR -dd $DIR -u $USER -c $WILD -h $HOST -l $LOG -i $PID -T $CSET $*

