'''
   alert card dynamically builted from content for ./targets_and_observables/targets.txt and ./targets_and_observables/observables.txt file
'''
import sys, os
    
def create_isolation_confirmation_card_content(card_title,observables):
    information_messages="You are about to isolate following Assets. Which can have an impact on users. Do you confirm this actions ?"
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
                                "text": information_messages,
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
                        "title": "Confirm Endpoint Isolation",
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
                                    "type": "TextBlock",
                                    "text": observables,
                                    "size": "Medium"
                                },                                                               
                                {
                                    "type": "Input.ChoiceSet",
                                    "id": "enforcement_points",  
                                    "style": "compact",
                                    "choices": [
                                        {
                                            "title": "NO I DON'T CONFIRM",
                                            "value": "NO"
                                        },                                    
                                        {
                                            "title": "YES I Confirm",
                                            "value": "YES"
                                        }
                                    ],
                                    "placeholder": "Do you confirm ? :"
                                },
                                {
                                    "type":"ActionSet",
                                    "actions": [
                                        {
                                            "type": "Action.Submit",
                                            "title": "Send",
                                            "data": {
                                                "callback_keyword": "isolation_confirmed"
                                            }
                                        }
                                    ]                                
                                }
                            ],

                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
                        }
                    }             
                ]          
            }
        }
    ]    
    return(cards_content)
    
def create_ok_card_content():
    cards_content=[
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {    
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "backgroundImage": {
                    "url": "https://i.postimg.cc/CLbVWbZJ/check-ok.png",
                    "verticalAlignment": "Center"
                },             
                "id": "ok",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "\n\n\nOK DONE\n\n\n",
                        "weight": "Bolder",
                        "size": "ExtraLarge",                        
                        "horizontalAlignment": "Center"
                    }
               ]
            }
        }
    ]    
    return(cards_content)