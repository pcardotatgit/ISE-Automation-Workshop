# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : Add en new endpoint in and ANC Policy
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
    'accept': "application/json",
    'ERS-Media-Type':'anc.ancendpoint.1.0'
    }
username = ""
password = ""
host = ""
port = ""
#  def main***
def main():
    """
    MODIFIED : 2026-06-05T12:25:16.000Z
    description : starting point
    
    how to call it :
    """
    route="/main"
    env.level+="-"
    print("\n"+env.level,white("def main() in 6_ise_ers_add_endpoint_to_anc_policy.py : >\n",bold=True))
    loguer(env.level+" def main() in 6_ise_ers_add_endpoint_to_anc_policy.py : >")
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
    payload={} # <<<<<<<<<<<<<<<<<<< data to send to ISE, mainly for POST, PUT, PATCH calls 
    result_file_name='adding_host_to_anc_policy_result.json'
    method='put'
    relative_url='/ers/config/ancendpoint/apply' 

    mac_address="FC:FC:49:00:00:09"
    policynamelist="pxGridQRadarPortBounce"
    
    print("We want to add Endpoint : ",yellow(mac_address,bold=True),' to ANC Policy : ',yellow(policynamelist,bold=True))
    a=input('Press ENTER')
    
    payload = "{\r\n    \"OperationAdditionalData\": {\r\n    \"additionalData\": [{\r\n    \"name\": \"macAddress\",\r\n    \"value\": \""+ mac_address + "\"\r\n    },\r\n    {\r\n    \"name\": \"policyName\",\r\n    \"value\": \"" + policynamelist + '"' + "\r\n    }]\r\n  }\r\n}"

    
    api_url=f"https://{host}:{port}{relative_url}"
    a=input('\nWe are going to use a generic API function named send_api_call_function() in the code ( Press ENTER )')
    a=input('\nWe just have to customize the parameters we pass to it. See them here after ( Press ENTER )')
    print("\nusername : ",username)
    print("password : ",password)    
    #print("\nhost : ",host)
    #print("\nport : ",port)
    print("method : ",method)
    print("headers : ",headers)
    print("result_file_name in [ ./result ]: ",result_file_name)
    print("relative_url : ",yellow(relative_url,bold=True))
    print("payload : ",yellow(payload,bold=True)) 
    print("api_url : ",api_url)    
    requete=f"request({method}, {api_url}, headers={headers}, data = {payload}, verify=False)"
    print("request to send is :\n",yellow(requete,bold=True))       
    a=input('\nOkay Now lets send the API call and then manage the anwser and any error code ( Press ENTER)')
    print("\n===================================================================\n")
    result,response = send_api_call_function(username,password,method,api_url,headers,payload,result_file_name)
    print(green(response,bold=True)) 
    # ===================================================================
    #loguer(env.level+" def END OF main() in ise_apis_lab_1_ers_apis.py : >")    
    env.level=env.level[:-1]
    return 'ok'    

# def_parse_config_to_dict***
def parse_config_to_dict(config_json_file):
    '''
        version : 2026-03-05
        
        description : read the file input thru config_json_file and create a dictionnary that contains key names and their value from the json input
    '''
    env.level+='-'
    print(env.level,white('def parse_config_to_dict() in 6_ise_ers_add_endpoint_to_anc_policy.py  : >\n',bold=True))
    loguer(env.level+' def parse_config_to_dict() in 6_ise_ers_add_endpoint_to_anc_policy.py : > ')
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
    print(white('def send_api_call_function() in 6_ise_ers_add_endpoint_to_anc_policy.py  : >\n',bold=True))
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
        print(green('OKAY WE GOT A RESPONSE FROM ISE\n',bold=True))
        if '</title>' not in response.text:
            #json_txt_result = json.dumps(response.json(),indent=4,sort_keys=True, separators=(',', ': '))
            print(green('Assignment to policy Done',bold=True))
            json_txt_result=response.text			
            #print('json_txt_result  : \n',green(json_txt_result,bold=True))    
            # SAVE RESULT
            #with open('./results/'+result_file_name,'w') as file:
            #    file.write(json_txt_result)
        else:	
            json_txt_result=response.text
            print(white('Check the Endpoint ANC Policy Assignment in ISE',bold=True))
    # ===================================================================
    return result,json_txt_result

if __name__=="__main__":
    print(env.level,white("\nMAIN FUNCTION ( the Add Endpoint to ANC Policy application starts here ): >",bold=True))
    with open("./debug/log.txt","w") as file:
        pass
    loguer(env.level+"APPLICATION STARTS - Add Endpoint to ANC Policy ")
    main()
    print(green('\nOK DONE : Check the Endpoint ANC Policy Assignment in ISE',bold=True))
