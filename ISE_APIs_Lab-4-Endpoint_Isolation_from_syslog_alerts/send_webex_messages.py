# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : send alert messages to webex room
'''
import env as env
from crayons import *
from analyse_application_logs import loguer
import requests
import sys, os
from crayons import *
import json

# def_parse_config_to_dict***
def parse_config_to_dict(config_json_file):
    '''
        version : 2026-03-05
        
        description : read the file input thru config_json_file and create a dictionnary that contains key names and their value from the json input
    '''
    env.level+='-'
    print(env.level,white('def parse_config_to_dict() in send_webex_messages.py  : >\n',bold=True))
    loguer(env.level+' def parse_config_to_dict() in send_webex_messages.py  : > ')
    with open(config_json_file, 'r') as f:
        conf_result=json.load(f)   
    print(green(conf_result,bold=True))
    env.level=env.level[:-1]
    return conf_result



#  def create_card_content***
def create_card_content(card_title,alert_message,targets,observables):
    """
    MODIFIED : 2026-06-22T09:22:25.000Z

    description : create a alert card
    
    how to call it :
    """
    route="/create_card_content"
    env.level+="-"
    print("\n"+env.level,white("def create_card_content() in send_webex_messages.py : >\n",bold=True))
    loguer(env.level+" def create_card_content() in send_webex_messages.py : >")
    cards_content=[
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {    
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "backgroundImage": {
                    "url": "https://i.postimg.cc/vBxnRp06/sky2.jpg",
                    "verticalAlignment": "Center"
                },             
                "id": "title",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": card_title,
                        "color": "Attention",
                        "weight": "Bolder",
                        "size": "ExtraLarge",                        
                        "horizontalAlignment": "Center"
                    },
                    {
                        "type": "Container",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": alert_message,
                                "wrap": True,
                                "color": "Attention",
                                "horizontalAlignment": "Center"
                            }
                        ]
                    }                   
                ],
                "actions": [
                    {
                        "type": "Action.ShowCard",
                        "title": "Targeted Systems",
                        "card": {
                            "type": "AdaptiveCard",
                            "body": [
                                {
                                    "type": "TextBlock",
                                    "text": "Select Systems to isolate",
                                    "color": "Warning",
                                    "size": "Medium",
                                    "wrap": True
                                },
                                {
                                    "type": "Input.ChoiceSet",
                                    "id": "targets",
                                    "style": "expanded",
                                    "isMultiSelect": True,
                                    "choices": targets
                                }
                            ],
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Isolate Selected Systems",
                                    "data": {
                                        "callback_keyword": "Targets"
                                    }
                                }
                            ],
                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
                        }
                    },
                    {
                        "type": "Action.ShowCard",
                        "title": "Suspicious observables",
                        "card": {
                            "type": "AdaptiveCard",
                            "body": [
                                {
                                    "type": "TextBlock",
                                    "text": "Suspicious Observables :",
                                    "color": "Warning",
                                    "size": "Medium",
                                    "wrap": True
                                },
                                {
                                    "type": "Input.ChoiceSet",
                                    "id": "observables",
                                    "style": "expanded",
                                    "isMultiSelect": True,
                                    "choices": observables
                                }
                            ],
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Block Selected Objects",
                                    "horizontalAlignment": "Center",
                                    "data": {
                                        "callback_keyword": "observables"
                                    }
                                }
                            ],
                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
                        }
                    }                
                ]          
            }
        }
    ]    
    env.level=env.level[:-1]    
    return(cards_content)


#  def load_card_and_send_it***
def load_card_and_send_it(card_title,cards_content,WEBEX_BOT_TOKEN,ROOM_ID):
    """
    MODIFIED : 2026-06-22T09:25:39.000Z

    description : Lard an adaptive card an send it to webex room
    
    how to call it :
    """
    route="/load_card_and_send_it"
    env.level+="-"
    print("\n"+env.level,white("def load_card_and_send_it() in send_webex_messages.py : >\n",bold=True))
    loguer(env.level+" def load_card_and_send_it() in send_webex_messages.py : >")
    headers = {'Authorization': 'Bearer ' + WEBEX_BOT_TOKEN,
               'Content-type': 'application/json;charset=utf-8'}
    print(cyan(cards_content))
    attachment={
    "roomId": ROOM_ID,
    "markdown": card_title,
    "attachments": cards_content
    }
    response = requests.post("https://webexapis.com/v1/messages", json=attachment,headers=headers)
    if response.status_code == 200:
        # Great your message was posted!
        #message_id = response.json['id']
        #message_text = response.json['text']
        print("New message created")
        #print(message_text)
        print("====================")
        print(response)
        result=1
    else:
        # Oops something went wrong...  Better do something about it.
        print(response.status_code, response.text)
        result=0        
    env.level=env.level[:-1]
    return result

#  def send_alert***
def send_alert(observables):
    """
    MODIFIED : 2026-06-22T09:29:14.000Z

    description : send an alert to webex
    
    how to call it : result = send_alert(observables)
    """
    route="/send_alert"
    env.level+="-"
    print("\n"+env.level,white("def send_alert() in send_webex_messages.py : >\n",bold=True))
    loguer(env.level+" def send_alert() in send_webex_messages.py : >")
    target_list=create_observables_list(observables)
    observable_list=target_list
    alert_message='We found an infected Endpoint, Do you want to isolate it ?'
    config=parse_config_to_dict('./webex_config.json')    
    card_title='Endpoint Isolation Request'    
    card_content=create_card_content(card_title,alert_message,target_list,observable_list)
    load_card_and_send_it(card_title,card_content,config["WEBEX_BOT_TOKEN"],config["ALERT_ROOM_ID"])
    result = 1
    env.level=env.level[:-1]
    return result

#  def create_observables_list***
def create_observables_list(observables):
    """
    MODIFIED : 2026-06-22T09:41:31.000Z

    description : create an observable list from the text string in input
    
    how to call it :
    """
    route="/create_observables_list"
    env.level+="-"
    print("\n"+env.level,white("def create_observables_list() in send_webex_messages.py : >\n",bold=True))
    loguer(env.level+" def create_observables_list() in send_webex_messages.py : >")
    print("\nobservables : ",observables)
    observable_list=[] 
    object_list=[]
    if '\n' in observables:
        object_list=text_content.split('\n')
    elif ',' in observables:
        object_list=text_content.split(',')     
    elif ';' in observables:
        object_list=text_content.split(';') 
    else:
        object_list.append(observables)
    for item in object_list:
        print(item)
        objet={"title": item,"value": item}
        observable_list.append(objet)
    print("\nobservable_list : ",observable_list)
    env.level=env.level[:-1]    
    return(observable_list)


