
#!/bin/bash

#ensure sudo
ip link set wpan0 down
ip link set lowpan0 down
iwpan phy phy0 set channel 0 16 #Set the device to use page 0 and channel 16
ip link add link wpan0 lowpan0 type lowpan
iwpan dev wpan0 set pan_id 0xbeef #Cmd will echo usage
iwpan dev lowpan0 set pan_id 0xbeef #All devices must have the same pan_id
ip link set wpan0 up
ip link set lowpan0 up
sh -c "echo 1 > /proc/sys/net/ipv6/conf/all/forwarding"
ip address add dead:beef:dead:beef::1/64 dev lowpan0
#simpleRPL CLI is bound by this script to the execution directory
sudo simpleRPL.py -vvvvv -R -d dead:beef:dead:beef::1 -p dead:beef:dead:beef:: -i lowpan0
