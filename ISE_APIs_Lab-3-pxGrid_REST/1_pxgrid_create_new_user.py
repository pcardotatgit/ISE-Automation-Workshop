# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : Create a nex pxGrid client
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
    print("\n"+env.level,white("def main() in 1_pxgrid_create_new_user.py : >\n",bold=True))
    loguer(env.level+" def main() in 1_pxgrid_create_new_user.py : >")
    global username
    global password
    global host
    global port
    # ===================================================================    
    #policylist = ise_get_anc_policies()
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
    a=input('\nStep - 1 : lets check that we have already created the new user. If not then lets create it in ISE, Credentials will be stored in ./z_pxgrid-creds.txt')
    
    
    # Check if the credentials file exists
    if not os.path.exists("z_pxgrid-creds.txt"):
        print("\nz_pxgrid-creds.txt does not exist, then lets create an new pxgrid account\n")
        a=input('\nWe have to create a New pxGrid client')
        print(red('\nNotice : 503 error might indicate that in ISE pxGrid setting [ Allow password based account creation ] is not enabled !\nOr new pxGrid client is in initiate state then continue',bold=True))
        a=input('\nPress Enter to continue')
        # Create new pxGrid username
        r = requests.post(f"{api_url}/AccountCreate",
            headers=headers,
            verify=False,
            json=payload
        )

        # Raise an exception for HTTP errors
        r.raise_for_status()
        password = r.json()["password"]

        # Save the credentials to a file
        with open("z_pxgrid-creds.txt", "w") as f:
            f.write(f"{new_pxgrid_client}:{password}")    
    # Read the credentials from the file
    with open("z_pxgrid-creds.txt", "r") as f:
        pxgrid_username, pxgrid_password = f.read().strip().split(":")  
    a=input('\nOkay lets activate the new pxGrid Client if not already done')
    print("\npxgrid_username : ",pxgrid_username) 
    print("\npxgrid_password assigned by ISE : ",pxgrid_password) 
    print(yellow('\nStep - 2 : Now we are going to enter into a loop that will end when the new user has been enabled in ISE',bold=True))
    a=input('\nPress Enter to continue')

    #print("\nusername : ",username) 
    #print("\npassword: ",password) 
    
    # Repeat Activation process until client is approved
    while True:
        # Send Account Activate request
        r=requests.post(f"{api_url}/AccountActivate",
            verify=False,
            auth=(pxgrid_username,pxgrid_password), 
            json={}
        )
        r.raise_for_status()
        json_response=r.json()
        print(json.dumps(json_response,indent=2))
        if json_response["accountState"]=="ENABLED":
            print(green("New pxGrid Account Approved.",bold=True))
            break
        # Wait for 1 seconds before retrying
        sleep(1)    
    # ===================================================================
    #loguer(env.level+" def END OF main() in 1_pxgrid_create_new_user.py : >")    
    env.level=env.level[:-1]
    return 'ok'    

# def_parse_config_to_dict***
def parse_config_to_dict(config_json_file):
    '''
        version : 2026-03-05
        
        description : read the file input thru config_json_file and create a dictionnary that contains key names and their value from the json input
    '''
    env.level+='-'
    print(env.level,white('def parse_config_to_dict() in 1_pxgrid_create_new_user.py  : >\n',bold=True))
    loguer(env.level+' def parse_config_to_dict() in 1_pxgrid_create_new_user.py : > ')
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
    print(white('def send_api_call_function() in 1_pxgrid_create_new_user.py  : >\n',bold=True))
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
    print(env.level,white("\nMAIN FUNCTION ( the create new pxgrid user application starts here ): >",bold=True))
    with open("./debug/log.txt","w") as file:
        pass
    loguer(env.level+"APPLICATION STARTS - create new pxgrid user")
    main()
    print(green('\nOK DONE : check result in [ ./result/create_new_user.json ]',bold=True))

