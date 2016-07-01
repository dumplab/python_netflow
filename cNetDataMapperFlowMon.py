"""Connection to your FlowMon host - requires requests for REST calls

This class gives you an idea how to use FlowMon REST API ... please read FlowMon REST API developers guide for more informations
"""

__author__    = "dumplab"
__copyright__ = "2016 dumplab"
__license__   = "MIT"
__version__   = "0.1"
__status__    = "Development"

import time,json,re,requests
from flowmonconfig import FLOWMON_HOST,FLOWMON_REST_USER,FLOWMON_REST_PASS

class cNetDataMapperFlowMon:
        """The mapper between FlowMon and ..."""

        def __init__(self):
		"""Set default attribute values only
		
		No arguments
		"""
		self.__controller = FLOWMON_HOST
		self.__username   = FLOWMON_REST_USER
		self.__password   = FLOWMON_REST_PASS
		self.__token      = None
		self.__debugging  = False

	def __getAuthToken(self):
		"""Get a Authentication Token from FlowMon"""
		self.__token=None
		#specify the username and password which will be included in the data. 
		payload = {"username":self.__username,"password":self.__password,"grant_type":"password","client_id":"invea-tech"}
		#This is the URL to get the authentication token.  
		url = "https://" + self.__controller + "/resources/oauth/token"
		#SSL certification is turned off, but should be active in production environments
		response=requests.post(url,payload, verify=False)
		#Check if a response was received. If not, print an error message.
		if(not response):
			if self.__debugging == True:
				print ("No data returned while fetching token!")
		else:
			#Data received.  Get the token
			r_json=response.json()
			self.__token = r_json["access_token"]
			if self.__debugging == True:
				print("Token: " + str(self.__token))

	def getChart(self):
		# see if we already got a token
		if self.__token is None:
	                self.__getAuthToken()
                if(self.__token):
			header  = {"Authorization": "bearer " + self.__token}
			payload = {"from":self.__getTodayString() + " 00:00","to":self.__getNowString(),"profile": "live","chart": { "measure": "traffic","protocol": 1}}
			url      = "https://" + self.__controller + "/rest/fmc/analysis/chart"
       	                #Get 
			response = requests.get(url+"?search="+json.dumps(payload),headers=header,verify=False)
			if response.status_code==200:
				if self.__debugging == True:
					print("Response: " + str(response.content))
				return json.loads(response.content)
               	else:
			print("No authentication token was received.")

	def getActiveDevicesByAddress(self,address=None,limit=50):
		"""getActiveDevicesByAddress - return activeDevices seen today json
		
		Keyword arguments:
		address -- could be and IPv4 IPv4 w/ CIDR notation or mac address in format xy:xy:xy:xy:xy
		limit   -- returned limit - default 50
		"""
		if address==None:
			return False
		# get token
		if self.__token is None:
			self.__getAuthToken()
		if(self.__token):
			header   = {"Authorization": "bearer " + self.__token}
			payload  = {"from":self.__getTodayString() + " 00:00","to":self.__getNowString(),"device": address}
			url      = "https://" + self.__controller + "/rest/fmc/activeDevices?limit=" + str(limit)
			response = requests.get(url+"&search="+json.dumps(payload),headers=header,verify=False)
			if response.status_code==200:
				if self.__debugging == True:
					print("Response: " + str(response.content))
				return json.loads(response.content)
			else:
				return None
		else:
			print("No authentication token was received.")

	def __getTodayString(self):
		"""__getTodayString - return somethin like 2016-08-01 as a string
		
		No arguments
		"""
		return time.strftime("%Y-%m-%d")

	def __getNowString(self):
		"""__getNowString - return something like 2016-08-01 12:24 as a string
		
		No arguments
		"""
		return time.strftime("%Y-%m-%d %H:%M")

