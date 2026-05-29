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
password = "cisco123"
host = "198.18.133.27"
port = "443"

# Functions
def ise_get_anc_policies():
    authentication = HTTPBasicAuth(username, password)
    url = f"https://{host}:{port}/ers/config/ancpolicy"
    
    #Create GET Request 
    req = requests.get(url, verify=False, auth=authentication, headers=headers)
    #req = requests.request("GET", url, verify=False, headers=headers)
    namelist = " "
    print(yellow('\nANC Policies in ISE :\n',bold=True))
    if(req.status_code == 200):
        resp_json = req.json()
        policies = resp_json["SearchResult"]["resources"]
        for policy in policies:
            namelist = policy["name"]
            print(namelist)   
    else:
        print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})
    return namelist


if __name__ == "__main__":
   #TODO Call the function for getting ANC policy and store it in the policylist variable
   policylist = ise_get_anc_policies()
   #TODO call the function for applying policy to the endpoints
   #post_to_ise(maclist, policylist)
   print(green("\nOKAY DONE!!!",bold=True))