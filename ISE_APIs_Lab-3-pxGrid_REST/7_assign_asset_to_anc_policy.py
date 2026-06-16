# https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/ANC-configuration
import requests
import json
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from crayons import *

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

pxgrid_hostname = '198.18.133.27'
pxgrid_url = f"https://{pxgrid_hostname}:8910/pxgrid/control"

# Read the credentials from the file
with open("z_pxgrid-creds.txt", "r") as f:
    username, password = f.read().strip().split(":")

a=input('\nLets do a service lookup on the com.cisco.ise.config.anc service')
# Lookup trustsec service
r=requests.post(f"{pxgrid_url}/ServiceLookup",
    verify=False,
    auth=(username,password),
    json={
        "name": "com.cisco.ise.config.anc"
    }
)

# Raise an exception for HTTP errors
r.raise_for_status()

# Display the response
print(cyan(json.dumps(r.json(),indent=2),bold=True))

a=input('\nOkay Now lets get the service information\n  - First lets prepare the variable for the next apiu calls,\n     from the answer we got prior')
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
a=input('\nOkay Now lets retreive the AccessSecret assigned to our pxGrid node ')

# Get Access Secret
r=requests.post(f"{pxgrid_url}/AccessSecret",
    verify=False,
    auth=(username,password),
    json={
        "peerNodeName": node_name
    }
)
r.raise_for_status()
secret=r.json()["secret"]

print("\nOkay, secret : ",yellow(secret,bold=True))

a=input('\nOkay Ready !, lets assign host: 11:22:33:44:55:66 to ANC-Quarantine policy')

rest_url='https://'+pxgrid_hostname+":8910/pxgrid/ise/config/anc"

endpoint_to_anc_policy={
        "policyName": "ANC-Quarantine",
        "macAddress":"11:22:33:44:55:66"
    }

# Apply ANC policy
r=requests.post(f"{rest_url}/applyEndpointByMacAddress",
    verify=False,
    auth=(username,secret),
    json=endpoint_to_anc_policy
)

# Raise an exception for HTTP errors
r.raise_for_status()

# Display the response
print(cyan(json.dumps(r.json(),indent=2),bold=True))
print(white('\nCHECK Endpoint assignment in ISE',bold=True))