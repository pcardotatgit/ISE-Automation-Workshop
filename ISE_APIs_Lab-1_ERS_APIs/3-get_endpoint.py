#!/usr/bin/env python
'''
    version : 2026-05-06
    description : Generic API call to ISE
'''
import json
import sys
from pathlib import Path

import requests
from crayons import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." / "..").resolve()

sys.path.insert(0, str(repository_root))

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Functions

headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }
username = "api_admin"
password = "ChangeMe"
host = "198.18.133.27"
port = "443"

#print missing mission warning!
#MISSION = print_missing_mission_warn()

def get_users_in_ise():
    
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

#  def_send_api_call_function***
def send_api_call_function(username,password,method,api_url,headers,payload,result_file_name):
    '''
    MODIFIED : 2026-04-15
    description : send_the_api call to the destination REST service
    
    how to call it : result,json_txt_result=send_api_call_function(username,password,method,api_url,headers,payload)
    '''
    print()
    print(white('def send_api_call_function() in app.py  : >\n',bold=True))
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
            json_txt_result = json.dumps(response.json(),indent=4,sort_keys=True, separators=(',', ': '))
            #print('json_txt_result  : \n',green(json_txt_result,bold=True))    
            # SAVE RESULT
            with open('./results/'+result_file_name,'w') as file:
                file.write(json_txt_result)
        else:
            json_txt_result=response.text
            print(red('But something seems to be wrong',bold=True))
            print('RESULT : ',red(response_txt,bold=True))
    # ===================================================================
    return result,json_txt_result
    

if __name__ == "__main__":
    method='get' # <<<<<<<<<<<<<<<<<<<< method to use
    headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }
    payload={} # <<<<<<<<<<<<<<<<<<< data to send to ISE, mainly for POST, PUT, PATCH calls   
    result_file_name='endpoints.json'
    relative_url='/ers/config/endpoint' # <<<<<<<<<<<<<<<<<<<<<<<<<<< Relative URL here
    api_url=f"https://{host}:{port}{relative_url}"

    result,response = send_api_call_function(username,password,method,api_url,headers,payload,result_file_name)
    print(green(response,bold=True))
    #TODO call the function for applying policy to the endpoints
    #post_to_ise(maclist, policylist)
    print(white("\n-------- OPERATION DONE -----------",bold=True))