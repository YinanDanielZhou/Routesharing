#!/bin/sh

# sudo tc qdisc add dev eth0 root netem delay 100ms     # This simulates the outbound not the inbound !

python -u run_server.py $COORD_URL $HOST_IP $HOST_PORT_TO_BIND
# -u run_server.py coord_ip:coord_port host_ip host_port 
# -u is used to diable python stdout buffering