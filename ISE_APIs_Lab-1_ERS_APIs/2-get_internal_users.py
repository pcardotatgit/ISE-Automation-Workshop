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

def get_users_ise():
    
    #TODO: finish the URL for the GET request to get the ANC policy from ISE
    authentication = HTTPBasicAuth(username, password)
    url = f"https://{host}:{port}/ers/config/internaluser"
    
    #Create GET Request 
    req = requests.get(url, verify=False, auth=authentication, headers=headers)
    #req = requests.request("GET", url, verify=False, headers=headers)
    namelist = " "
    if(req.status_code == 200):
        resp_json = req.json()
        print(resp_json)   
    else:
        print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})
    return namelist


if __name__ == "__main__":
   #TODO Call the function for getting ANC policy and store it in the policylist variable
   users = get_users_ise()
   #TODO call the function for applying policy to the endpoints
   #post_to_ise(maclist, policylist)
   print(green("ISE Mission Completed!!!"))