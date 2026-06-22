# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : Get All ANC Policies configured in the ISE server
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
#  def ise_get_anc_policies***
def ise_get_anc_policies(username,password,host,port):
    """
    MODIFIED : 2026-06-05T12:23:37.000Z

    description : get all ANC policies configured in ISE server
    
    how to call it : anc_policies=ise_get_anc_policies(username,password,host,port)
    """
    route="/ise_get_anc_policies"
    env.level+="-"
    print("\n"+env.level,white("def ise_get_anc_policies() in 1_ise_ers_get_all_anc_policies.py : >\n",bold=True))
    loguer(env.level+" def ise_get_anc_policies() in 1_ise_ers_get_all_anc_policies.py : >")
    # ===================================================================    
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
            print(cyan('- '+namelist,bold=True))   
    else:
        print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})
    # ===================================================================
    #loguer(env.level+" def END OF ise_get_anc_policies() in ise_apis_lab_1_ers_apis.py : >")    
    env.level=env.level[:-1]
    return namelist
    

#  def main***
def main():
    """
    MODIFIED : 2026-06-05T12:25:16.000Z
    description : starting point
    
    how to call it :
    """
    route="/main"
    env.level+="-"
    print("\n"+env.level,white("def main() in 1_ise_ers_get_all_anc_policies.py : >\n",bold=True))
    loguer(env.level+" def main() in 1_ise_ers_get_all_anc_policies.py : >")
    global username
    global password
    global host
    global port
    # ===================================================================    
    #policylist = ise_get_anc_policies()
    config=parse_config_to_dict('./config.json')
    username = config["username"]
    password = config["password"]
    host = config["host"]
    port = config["port"]
    policylist=ise_get_anc_policies(username,password,host,port)
    
    # ===================================================================
    #loguer(env.level+" def END OF main() in ise_apis_lab_1_ers_apis.py : >")    
    env.level=env.level[:-1]
    return policylist

# def_parse_config_to_dict***
def parse_config_to_dict(config_json_file):
    '''
        version : 2026-03-05
        
        description : read the file input thru config_json_file and create a dictionnary that contains key names and their value from the json input
    '''
    env.level+='-'
    print(env.level,white('def parse_config_to_dict() in 1_ise_ers_get_all_anc_policies.py  : >\n',bold=True))
    loguer(env.level+' def parse_config_to_dict() in 1_ise_ers_get_all_anc_policies.py : > ')
    with open(config_json_file, 'r') as f:
        conf_result=json.load(f)   
    print(green(conf_result,bold=True))
    env.level=env.level[:-1]
    return conf_result


if __name__=="__main__":
    print(env.level,white("\nMAIN FUNCTION ( the get all ANC policies application starts here ): >",bold=True))
    with open("./debug/log.txt","w") as file:
        pass
    loguer(env.level+"APPLICATION STARTS - get all ANC policies ")
    main()
    print(green('\nOK DONE',bold=True))
