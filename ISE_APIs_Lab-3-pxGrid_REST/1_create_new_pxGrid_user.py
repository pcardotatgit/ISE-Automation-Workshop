# Reference: https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/pxGrid-Consumer

import requests
import json
from time import sleep
import os
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#global variables
headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }
username = "admin"
password = "ChangeMe"
host = "198.18.133.27"
port = "443"
authentication = HTTPBasicAuth(username, password)
pxgrid_hostname = '198.18.133.27'
pxgrid_url = f"https://{pxgrid_hostname}:8910/pxgrid/control"

# Check if the credentials file exists
if not os.path.exists("z_pxgrid-creds.txt"):
    print("z_pxgrid-creds.txt does not exist, then lets create an new pxgrid account")
    a=input('Next ?')
    # Create new pxGrid username
    r = requests.post(f"{pxgrid_url}/AccountCreate",
        headers=headers,
        verify=False,
        json={
            "nodeName": "pxgrid-client-pwd",
        }
    )

    # Raise an exception for HTTP errors
    r.raise_for_status()
    password = r.json()["password"]

    # Save the credentials to a file
    with open("z_pxgrid-creds.txt", "w") as f:
        f.write(f"pxgrid-client-pwd:{password}")

# Read the credentials from the file
with open("z_pxgrid-creds.txt", "r") as f:
    username, password = f.read().strip().split(":")


# Repeat Activation process until client is approved
while True:
    # Send Account Activate request
    r=requests.post(f"{pxgrid_url}/AccountActivate",
        verify=False,
        auth=(username,password), 
        json={}
    )
    r.raise_for_status()
    json_response=r.json()
    print(json.dumps(json_response,indent=2))
    if json_response["accountState"]=="ENABLED":
        print(f"Account Approved.")
        break

    # Wait for 60 seconds before retrying
    sleep(1)
