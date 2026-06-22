# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : pxgrid resources for the ise endpoint isolation from FTD syslogs
                    Add an endpoint to an ISE ANC Policy
'''

import env as env
from crayons import *
from analyse_application_logs import loguer
import json
import sys
from pathlib import Path
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
import os
from time import sleep

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#global variables
headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

username = ""
password = ""
host = ""
port = ""

#  def quarantine_endpoint***
def quarantine_endpoint(endpoint_ip_address):
    """
    MODIFIED : 2026-06-21T17:31:12.000Z

    description : Quarantine endpoint by IP address in ISE
    
    how to call it :
    """
    route="/quarantine_endpoint"
    env.level+="-"
    print("\n"+env.level,white("def quarantine_endpoint() in pxgrid_resources.py : >\n",bold=True))
    loguer(env.level+" def quarantine_endpoint() in pxgrid_resources.py : >")
    # ===================================================================    
    print(yellow('REFERENCE : https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/ANC-configuration',bold=True),'\n')
    a=input('Is the ISE server IP address is 198.18.133.27 ? Press Enter to confirm or enter the correct ip address : ')
    if a=='':
        pxgrid_hostname='198.18.133.27'
    else:
        pxgrid_hostname=a
    api_url=f"https://{pxgrid_hostname}:{port}{relative_url}"
    
    print('api_url : ',yellow(api_url,bold=True))
    
    print('\nStep - 1 : lets check that we already created the pxGrid user. If not will will have to create one')
        
    # Check if the credentials file exists
    if not os.path.exists("z_pxgrid-creds.txt"):
        print(red("\nERROR no z_pxgrid-creds.txt file found in the syslog server directory !\n",bold=True))
        print(yellow("\n=> Copy it from Lab 3 into the syslog server directory OR Run again Lab 3 from this directory to create a new pxgrid client\n",bold=True))
        sys.exit()
    else:
        # Read the credentials from the file
        with open("z_pxgrid-creds.txt", "r") as f:
            pxgrid_username, pxgrid_password = f.read().strip().split(":")     
            
    print('\nLets do a service lookup on the com.cisco.ise.config.anc service')
    
    print("\npxgrid_username : ",pxgrid_username) 
    print("\npxgrid_password assigned by ISE : ",pxgrid_password) 
    
    # Lookup trustsec service
    r=requests.post(f"{api_url}/ServiceLookup",
        verify=False,
        auth=(pxgrid_username,pxgrid_password),
        json={
            "name": "com.cisco.ise.config.anc"
        }
    )

    # Raise an exception for HTTP errors
    r.raise_for_status()

    # Display the response
    print(cyan(json.dumps(r.json(),indent=2),bold=True))

    print('\nOkay Now lets get the service information\n  - First lets prepare the variable for the next api calls,\n     from the answer we got prior')
    # Get the service information
    service_info=r.json()["services"][0]
    print("\nservice_info : ",cyan(service_info,bold=True)) 
    # Get the restBaseUrl
    rest_url=service_info["properties"]["restBaseUrl"]
    print("\nrest_url : ",rest_url)
    print("  - We need to tweak it a little bit to fit to the DCLOUD Lab")
    print("    - Lets replace keyword : ise.securitydemo.net with the ISE IP address which is : "+pxgrid_hostname)
    rest_url=rest_url.replace("ise.securitydemo.net",pxgrid_hostname)
    print("\nCorrect rest_url for DCLOUD Lab: ",cyan(rest_url,bold=True))
    # Get the nodeName
    node_name=service_info["nodeName"]
    print("\nnode_name : ",cyan(node_name,bold=True))
    print('\nOkay Now lets retreive the AccessSecret assigned to our pxGrid node ')

    # Get Access Secret
    r=requests.post(f"{api_url}/AccessSecret",
        verify=False,
        auth=(pxgrid_username,pxgrid_password),
        json={
            "peerNodeName": node_name
        }
    )
    r.raise_for_status()
    pxgrid_secret=r.json()["secret"]

    print("\nOkay, secret to for this pxgrid client is : ",yellow(pxgrid_secret,bold=True))
   
    print("\npxgrid_username : ",pxgrid_username) 
    print("\npxgrid secret : ",pxgrid_secret) 
    
    print('\nOkay Ready !, lets add endpoint ',yellow(endpoint_ip_address,bold=True),'to ANC policy :',yellow("ANC-Quarantine",bold=True))

    rest_url=f'https://{pxgrid_hostname}:8910/pxgrid/ise/config/anc/applyEndpointByIpAddress'

    print('api url to use is : ',yellow(rest_url,bold=True))

    endpoint_to_anc_policy={
        "policyName": "ANC-Quarantine",
        "ipAddress":endpoint_ip_address
    }
    # Create new ANC policy
    r=requests.post(rest_url,
        verify=False,
        auth=(pxgrid_username,pxgrid_secret),
        json=endpoint_to_anc_policy
    )

    # Raise an exception for HTTP errors
    r.raise_for_status()
    
    response_txt=json.dumps(r.json(),indent=2)
    # Display the response
    print(cyan(response_txt,bold=True))
    # save the response
    with open('./result/add_endpoint_to_anc_policy.json','w') as file:
        file.write(response_txt)
    env.level=env.level[:-1]
    result = 'ok'    
    # ===================================================================
    env.level=env.level[:-1]
    return result


