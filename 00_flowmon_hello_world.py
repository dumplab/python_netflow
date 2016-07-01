#!/usr/bin/python
from cNetDataMapperFlowMon import *

# connect to flow mon REST API and retrieve todays chart
flowMap = cNetDataMapperFlowMon()
data    = flowMap.getChart()
print(json.dumps(data, indent=4))
