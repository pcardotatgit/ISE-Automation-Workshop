# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : webex bot for managing ISE Endpoint isolation
'''
from webex_bot.webex_bot import WebexBot
from engine import cmd1,cmd2
import sys
from utils import *
from crayons import *
from analyse_application_logs import *
import env as env

BOT_ACCESS_TOKEN = ""
DESTINATION_ROOM_ID = ""

#  def_run_bot***
def run_bot(WEBEX_BOT_TOKEN):
    """
    Created : 2026-03-05
    description : Run the webex bot
    """
    route="/run_bot"
    env.level+="-"
    print("\n"+env.level,white("def run_bot() in ***run_bot.py*** : >\n",bold=True))
    loguer(env.level+" def run_bot() in ***run_bot.py*** : >")
    bot = WebexBot(WEBEX_BOT_TOKEN)
    bot.add_command(cmd1())
    bot.add_command(cmd2())

    bot.run()
if __name__=="__main__":
    print(env.level,white("MAIN FUNCTION ( the webex bot starts here ): >",bold=True))
    with open("./debug/log.txt","w") as file:
        pass
    loguer(env.level+" APPLICATION STARTS")
    with open('./webex_bot_config.json', 'r') as f:
        conf_result=json.load(f)
    WEBEX_BOT_TOKEN=conf_result["webex_bot_token"]
    run_bot(WEBEX_BOT_TOKEN)

