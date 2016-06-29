"""Connection to your FlowMon host - requires requests for REST calls

This class gives you an idea how to use FlowMon REST API ... please read FlowMon REST API developers guide for more informations
"""

__author__    = "dumplab"
__copyright__ = "2016 dumplab"
__license__   = "MIT"
__version__   = "0.1"
__status__    = "Development"

import re
import requests
import json

class cNetDataMapperFlowMon:
        """The mapper between FlowMon and ..."""

        def __init__(self):
		"""Set default attribute values only
		
		No arguments
		"""
		self.__controller = "<your.flowmonhost>"
		self.__username   = "flowmonusrname"
		self.__password   = "flowmonpass"
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
                #If tocken was received get chart using profile live
                if(self.__token):
			header = {"Authorization": "bearer " + self.__token}
			payload = {"from":"2016-06-01 00:00","to": "2016-06-01 08:00","profile": "live","chart": { "measure": "traffic","protocol": 1}}
			#This is the URL to get the authentication token.  
			url = "https://" + self.__controller + "/rest/fmc/analysis/chart"
       	                #Get 
			response=requests.get(url+"?search="+json.dumps(payload),headers=header,verify=False)
#			response = self.__doRestCall(self.__ticket,"get", "https://" + self.__controller + "/rest/fmc/analysis/chart")
			if self.__debugging == True:
				print("Token: " + str(self.__token))
				print("Response: " + str(response))
				print("ResponseContent: " + str(response.content))
			print response.content

               	else:
               	        print("No service ticket was received.  Ending program!")

        def getActiveDevices(self):
                # see if we already got a token
                if self.__token is None:
                        self.__getAuthToken()
                #If ticket received get active device
                if(self.__token):
                        header = {"Authorization": "bearer " + self.__token}
                        payload = {"from":"2016-06-28 00:00","to": "2016-06-28 14:00","device": "10.10.10.0/24"}
                        url = "https://" + self.__controller + "/rest/fmc/activeDevices?limit=50"
                        response=requests.get(url+"&search="+json.dumps(payload),headers=header,verify=False)
                        if self.__debugging == True:
                                print("Token: " + str(self.__token))
                                print("Response: " + str(response))
                                print("ResponseContent: " + str(response.content))
                        print("ResponseContent: " + str(response.content))

                else:
                        print("No service ticket was received.  Ending program!")
