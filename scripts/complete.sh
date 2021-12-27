#/bin/bash

config_path=$(grep ^aria2.conf /usr/local/etc/rc.d/aria2 | cut -d '"' -f2)
/usr/local/bin/python $(dirname $0)/complete.py $config_path $1 $2 $3

