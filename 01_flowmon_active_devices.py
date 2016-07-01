#!/usr/bin/python
# this exmaple queries the ActiveDevice - provide an IPv4 CIDR or MAC address informat xx:yy:zz:xx:yy:zz
from cNetDataMapperFlowMon import *

flowMap = cNetDataMapperFlowMon()
data    = flowMap.getActiveDevicesByAddress("0/0")
print(json.dumps(data, indent=4))
