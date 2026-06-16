#!/usr/bin/env python

import json
import sys
from pathlib import Path
import requests
from crayons import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#global variables
headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }
username = "api_admin"
password = "ChangeMe"
host = "198.18.133.27"
port = "443"

# Functions
def ise_get_deployment_node():
    authentication = HTTPBasicAuth(username, password)
    url = f"https://{host}:{port}/api/v1/deployment/node"
    
    #Create GET Request 
    req = requests.get(url, verify=False, auth=authentication, headers=headers)
    #req = requests.request("GET", url, verify=False, headers=headers)
    namelist = " "
    print(yellow('\nGET DEPLOYMENT NODE :\n',bold=True))
    if(req.status_code == 200):
        resp_json = req.json()
        print(resp_json)   
    else:
        print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})
    return resp_json


if __name__ == "__main__":
   #TODO Call the function for getting ANC policy and store it in the policylist variable
   node = ise_get_deployment_node()
   #TODO call the function for applying policy to the endpoints
   #post_to_ise(maclist, policylist)
   print(green("\nOKAY DONE!!!",bold=True))