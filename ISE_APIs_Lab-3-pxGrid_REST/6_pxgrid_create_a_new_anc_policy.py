# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : Create a new ANC policy in ISE server
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
#  def main***
def main():
    """
    MODIFIED : 2026-06-08
    description : starting point
    
    how to call it :
    """
    route="/main"
    env.level+="-"
    print("\n"+env.level,white("def main() in 6_pxgrid_create_a_new_anc_policy.py : >\n",bold=True))
    loguer(env.level+" def main() in 6_pxgrid_create_a_new_anc_policy.py : >")
    global username
    global password
    global host
    global port
    # ===================================================================    
    print(yellow('REFERENCE : https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/ANC-configuration',bold=True),'\n')
    config=parse_config_to_dict('./config_pxgrid.json')
    username = config["username"]
    password = config["password"]
    pxgrid_hostname = config["host"]
    port = config["port"]

    result_file_name='create_new_user.json'
    method='post'
    relative_url='/pxgrid/control' 
    
    new_pxgrid_client="pxgrid-client-new"
    payload={"nodeName": new_pxgrid_client} 
    
    api_url=f"https://{pxgrid_hostname}:{port}{relative_url}"
    a=input('\nStep - 1 : lets check that we already created the pxGrid user. If not will will have to create one')
        
    # Check if the credentials file exists
    if not os.path.exists("z_pxgrid-creds.txt"):
        print(red("\nz_pxgrid-creds.txt does not exist, You create a new pxgrid client\nUse [ 1_pxgrid_create_new_user.py ] for this",bold=True))
        sys.exit()
    else:
        # Read the credentials from the file
        with open("z_pxgrid-creds.txt", "r") as f:
            pxgrid_username, pxgrid_password = f.read().strip().split(":")     
            
    a=input('\nLets do a service lookup on the com.cisco.ise.config.anc service')
    
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

    a=input('\nOkay Now lets get the service information\n  - First lets prepare the variable for the next api calls,\n     from the answer we got prior')
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
    
    print('\nOkay Ready !, lets create a new ANC Policy named : ',yellow('ANC-Quarantine',bold=True))
    a=input('\nPress Enter to continue')

    rest_url=f'https://{pxgrid_hostname}:8910/pxgrid/ise/config/anc/createPolicy'

    print('api url to use is : ',yellow(rest_url,bold=True))

    new_policy={
            "name": "ANC-Quarantine",
            "actions": ["QUARANTINE"]
        }
    # Create new ANC policy
    r=requests.post(rest_url,
        verify=False,
        auth=(pxgrid_username,pxgrid_secret),
        json=new_policy
    )

    # Raise an exception for HTTP errors
    r.raise_for_status()
    
    response_txt=json.dumps(r.json(),indent=2)
    # Display the response
    print(cyan(response_txt,bold=True))
    # save the response
    with open('./result/create_new_anc_policies.json','w') as file:
        file.write(response_txt)
    env.level=env.level[:-1]
    return 'ok'    

# def_parse_config_to_dict***
def parse_config_to_dict(config_json_file):
    '''
        version : 2026-03-05
        
        description : read the file input thru config_json_file and create a dictionnary that contains key names and their value from the json input
    '''
    env.level+='-'
    print(env.level,white('def parse_config_to_dict() in 6_pxgrid_create_a_new_anc_policy.py  : >\n',bold=True))
    loguer(env.level+' def parse_config_to_dict() in 6_pxgrid_create_a_new_anc_policy.py : > ')
    with open(config_json_file, 'r') as f:
        conf_result=json.load(f)   
    print(green(conf_result,bold=True))
    env.level=env.level[:-1]
    return conf_result


#  def send_api_call_function***
def send_api_call_function(username,password,method,api_url,headers,payload,result_file_name):
    '''
    MODIFIED : 2026-06-05
    description : send_the_api call to the destination REST service
    
    how to call it : result,json_txt_result=send_api_call_function(username,password,method,api_url,headers,payload)
    '''
    print()
    print(white('def send_api_call_function() in 6_pxgrid_create_a_new_anc_policy.py  : >\n',bold=True))
    # ===================================================================                                            
    #params=json.loads(params) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<< to troublshoot
    print(cyan('--> API CALL details here under :',bold=True))
    print('\nusername : ',yellow(username,bold=True))
    print('\npassword : ',yellow(password,bold=True))
    print('\napi_url : ',yellow(api_url,bold=True))    
    print('\nmethod : ',yellow(method,bold=True))     
    print('\npayload :',yellow(payload,bold=True))
    print('\nheaders :',yellow(headers,bold=True))    
    requete=f"request({method}, {api_url}, headers={headers}, data = {payload}, verify=False)"
    print("\n\nrequest to send :\n",yellow(requete,bold=True))  
    print("\n===================================================================\n")
    authentication = HTTPBasicAuth(username, password)
    response = requests.request(method, api_url, auth=authentication, headers=headers, data = payload, verify=False)
    print('response :',yellow(response,bold=True))
    print('response content :',yellow(response.content,bold=True))
    print() 
    response_txt='{}'

    if response.status_code==401:
        print(red('\nINVALID API CREDENTIALS !\n',bold=True))    
        result=0
        json_txt_result='{"Error":"Wrong Authentication"}'
    elif response.status_code==403:
        print(red('\nACCESS FORBIDEN !\n',bold=True))
        result=2
        json_txt_result=response.content       
    else:
        result=1
        print(green('OKAY WE GOT A RESPONSE FROM ISE',bold=True))
        if '</title>' not in response.text:
            #print(response.json())
            json_txt_result = json.dumps(response.json(),indent=4,sort_keys=True, separators=(',', ': '))
            #print('json_txt_result  : \n',green(json_txt_result,bold=True))    
            # SAVE RESULT
            with open('./result/'+result_file_name,'w') as file:
                file.write(json_txt_result)

        else:
            json_txt_result=response.text
            print(red('But something seems to be wrong',bold=True))
            print('RESULT : ',red(response_txt,bold=True))
    # ===================================================================
    return result,json_txt_result

if __name__=="__main__":
    print(env.level,white("\nMAIN FUNCTION ( the create a new anc policy  application starts here ): >",bold=True))
    with open("./debug/log.txt","w") as file:
        pass
    loguer(env.level+"APPLICATION STARTS - create a new anc policy ")
    main()
    print(green('\nOK DONE : Check ISE Policy List and check result in [ ./result/create_new_anc_policies.json ]',bold=True))

