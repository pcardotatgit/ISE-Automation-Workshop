# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : Get All Internal User from the ISE server
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
#  def get_ise_internal_users***
def get_ise_internal_users(username,password,host,port):
    """
    MODIFIED : 2026-06-05T12:23:37.000Z

    description : get all ANC policies configured in ISE server
    
    how to call it : internal_users=get_ise_internal_users(username,password,host,port)
    """
    route="/get_ise_internal_users"
    env.level+="-"
    print("\n"+env.level,white("def get_ise_internal_users() in 2_ise_ers_get_internal_users.py : >\n",bold=True))
    loguer(env.level+" def get_ise_internal_users() in 2_ise_ers_get_internal_users.py : >")
    # ===================================================================    
    authentication = HTTPBasicAuth(username, password)
    url = f"https://{host}:{port}/ers/config/internaluser"
    
    #Create GET Request 
    req = requests.get(url, verify=False, auth=authentication, headers=headers)
    #req = requests.request("GET", url, verify=False, headers=headers)
    namelist = " "
    print(yellow('\nANC Policies in ISE :\n',bold=True))
    if(req.status_code == 200):
        text_result=json.dumps(req.json(),sort_keys=True,indent=4, separators=(',', ': '))
        with open('./result/internal_users.json','w') as file:
            file.write(text_result)
        print(cyan(text_result,bold=True))   
    else:
        print("An error has ocurred with the following code %(error)s" % {'error': response.status_code})
    # ===================================================================
    #loguer(env.level+" def END OF get_ise_internal_users() in ise_apis_lab_1_ers_apis.py : >")    
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
    print("\n"+env.level,white("def main() in 2_ise_ers_get_internal_users.py : >\n",bold=True))
    loguer(env.level+" def main() in 2_ise_ers_get_internal_users.py : >")
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
    internal_users=get_ise_internal_users(username,password,host,port)
    
    # ===================================================================
    #loguer(env.level+" def END OF main() in ise_apis_lab_1_ers_apis.py : >")    
    env.level=env.level[:-1]
    return internal_users

# def_parse_config_to_dict***
def parse_config_to_dict(config_json_file):
    '''
        version : 2026-03-05
        
        description : read the file input thru config_json_file and create a dictionnary that contains key names and their value from the json input
    '''
    env.level+='-'
    print(env.level,white('def parse_config_to_dict() in 2_ise_ers_get_internal_users.py  : >\n',bold=True))
    loguer(env.level+' def parse_config_to_dict() in 2_ise_ers_get_internal_users.py : > ')
    with open(config_json_file, 'r') as f:
        conf_result=json.load(f)   
    print(green(conf_result,bold=True))
    env.level=env.level[:-1]
    return conf_result


if __name__=="__main__":
    print(env.level,white("\nMAIN FUNCTION ( the get internal users policies application starts here ): >",bold=True))
    with open("./debug/log.txt","w") as file:
        pass
    loguer(env.level+"APPLICATION STARTS - get internal users ")
    main()
    print(green('\nOK DONE : check result in [ ./result/internal_users.json ]',bold=True))

