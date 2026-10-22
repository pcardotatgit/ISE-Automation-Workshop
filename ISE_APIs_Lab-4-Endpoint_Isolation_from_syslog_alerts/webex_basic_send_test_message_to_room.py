# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : A very basic client that send text messages to webex with a BOT TOKEN for quick test
'''
import env as env
from crayons import *
from analyse_application_logs import loguer
import requests
import json

DESTINATION_ROOM_ID=""
BOT_ACCESS_TOKEN=""


#  def send_message_to_webex_room***
def send_message_to_webex_room(message,DESTINATION_ROOM_ID,BOT_ACCESS_TOKEN):
    """
    MODIFIED : 2026-10-22T15:36:26.000Z

    description : send message to webex room from bot token
    
    how to call it : result = send_message_to_webex_room(message,DESTINATION_ROOM_ID,BOT_ACCESS_TOKEN)
    """
    route="/send_message_to_webex_room"
    env.level+="-"
    print("\n"+env.level,white("def send_message_to_webex_room() in webex_basic_send_test_message_to_room.py : >\n",bold=True))
    loguer(env.level+" def send_message_to_webex_room() in webex_basic_send_test_message_to_room.py : >")
    # ===================================================================    
    print(cyan(f"BOT_ACCESS_TOKEN = {BOT_ACCESS_TOKEN}",bold=True))
    print(cyan(f"DESTINATION_ROOM_ID = {DESTINATION_ROOM_ID}",bold=True))
    print(cyan(f"MESSAGE= {message}",bold=True))
    #URL = 'https://api.ciscospark.com/v1/messages'
    URL = 'https://webexapis.com/v1/messages'

    headers = {'Authorization': 'Bearer ' + BOT_ACCESS_TOKEN,
               'Content-type': 'application/json;charset=utf-8'}
    post_data = {'roomId': DESTINATION_ROOM_ID,
                 'markdown': message_out}
    response = requests.post(URL, json=post_data, headers=headers)
    if response.status_code == 200:
        # Great your message was posted!
        #message_id = response.json['id']
        #message_text = response.json['text']
        print(green("New message succesfully sent",bold=True))
        #print(message_text)
        print("====================")
        print(response)
        result=1
    elif response.status_code == 401:
        print()
        print(red("Error bad authentication token",bold=True))   
        result=0
    else:
        # Oops something went wrong...  Better do something about it.
        print(red(response.status_code, response.text,bold=True))
        result=0
    # ===================================================================
    env.level=env.level[:-1]
    return result

# def_parse_config_to_dict***
def parse_config_to_dict(config_json_file):
    '''
        version : 2026-03-05
        
        description : read the file input thru config_json_file and create a dictionnary that contains key names and their value from the json input
    '''
    env.level+='-'
    print(env.level,white('def parse_config_to_dict() in webex_basic_send_test_message_to_room.py  : >\n',bold=True))
    loguer(env.level+' def parse_config_to_dict() in webex_basic_send_test_message_to_room.py  : > ')
    with open(config_json_file, 'r') as f:
        conf_result=json.load(f)   
    print(green(conf_result,bold=True))
    env.level=env.level[:-1]
    return conf_result



if __name__=="__main__":
    print(env.level,white("MAIN FUNCTION ( BASIC SEND TEST MESSAGE TO WEBEX ROOM starts here ): >",bold=True))
    '''
    with open("./debug/log.txt","w") as file:
        pass
    '''
    loguer(env.level+" BASIC SEND TEST MESSAGE TO WEBEX ROOM starts")
    webex_config=parse_config_to_dict('./webex_config.json')
    
    message_out="HTTP POST CALL EXAMPLE TEST FROM PYTHON SCRIPT"
    print("\nALERT_ROOM_ID : ",webex_config['ALERT_ROOM_ID']) 
    print("\nWEBEX_BOT_TOKEN : ",webex_config['WEBEX_BOT_TOKEN']) 
    print("\nmessage_out : ",message_out) 
    send_message_to_webex_room(message_out,webex_config['ALERT_ROOM_ID'],webex_config['WEBEX_BOT_TOKEN'])
    print('OK DONE')
