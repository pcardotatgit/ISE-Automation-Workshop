from webex_bot.models.command import Command
from webex_bot.models.response import Response
import logging
import requests
import json
import utils
from crayons import *
from adaptive_card import *
from analyse_application_logs import *

log = logging.getLogger(__name__)

class cmd1(Command):
    def __init__(self):
        super().__init__(
            command_keyword="targets",
            help_message="Confirm Targets ISE Isolation",
            card=None,
        )
    def execute(self, message, attachment_actions, activity):
        print('CMD 1 TRIGGERED')
        observables=attachment_actions.inputs['targets']
        print('observables : ',cyan(observables,bold=True))
        card_title="WARNING"
        cards_content=create_isolation_confirmation_card_content(card_title,observables)
        response = Response()
        response.text = "Endpoint Isolation Request"
        # Attachments being sent to user
        response.attachments = cards_content[0]
        return response
class cmd2(Command):
    def __init__(self):
        super().__init__(
            command_keyword="isolation_confirmed",
            help_message="Isolate selected host",
            card=None,
        )
    def execute(self, message, attachment_actions, activity):
        print('CMD 2 TRIGGERED')
        cards_content=create_ok_card_content()
        response = Response()
        response.text = "isolation confirmed"
        # Attachments being sent to user
        response.attachments = cards_content[0]
        return response
