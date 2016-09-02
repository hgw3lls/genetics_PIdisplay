#!/bin/bash

for int in `cat /proc/net/dev| grep : | cut -f1 -d:| awk '{ print $1 }'`
do 
  echo $int
  curl http://web.wtfoo.net/pear/check.igc?name=`hostname`-${int}\&ip=`/sbin/ifconfig ${int} | grep "inet addr" | cut -f2 -d: | cut -f1 -d" "` >/dev/null 2>&1
done
