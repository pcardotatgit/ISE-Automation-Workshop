# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : syslog server for the ISE API lab
'''
import env as env
from crayons import *
from analyse_application_logs import loguer
from crayons import *
import socketserver
from datetime import datetime, date, timedelta
import sys
from ftd_syslog_parser import *
from pxgrid_resources import *
from send_webex_messages import *

dateTime = datetime.now()
HOST, PORT = "0.0.0.0", 514
use_webex_bot=1

# here under syslog server functions
class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global use_webex_bot
        # get syslog message receive in the socket
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        syslog=str(data) # put it into the syslog variable
        # ok here under let's do basic parsing and let's keep only FTD IPS alerts BUT dont keep syslogs with 'PROTOCOL-DNS SPOOF query response with TTL of 1 min. and no authority'
        if '%FTD' in syslog and 'SID' in syslog and 'PROTOCOL-DNS SPOOF query response with TTL of 1 min. and no authority' not in syslog and 'PROTOCOL-DNS TMG Firewall Client long host entry exploit attempt' not in syslog and 'MALWARE-CNC DNS Fast Flux attempt' not in syslog:
            the_log=parse_ftd_single_log(syslog)    
        if '<END>' in syslog:
            with open('./bad_ip.txt') as file:
                internal_ip=file.read()
            print('\n===========================================\n\nAttacker IP addresses Detected by IPS : \n')
            for ip in infected_machine_list:
                if ip==internal_ip:
                    print(red('- '+ip+' : This is an internal ip address ! this infected Endpoint will be Quarantined in ISE !!',bold=True))
                    infected_ip_address=ip
                else:    
                    print('-',ip)
            print('\n===========================================')
            print(yellow('- Use pxGrid REST APIs and query Cisco ISE for quarantine for : '+ip,bold=True))
            a= input('\nDo You want ISE to add this ip Address to the ANC Policy ? Y / N : ')
            if a=='Y' or a=='y':  
                if use_webex_bot:
                    print(yellow('\n- You decided to send an alert to webex',bold=True))
                    result=send_alert(infected_ip_address) # send an alert to webx for Endpoint Isolation Approval
                    result = { 'status':'Alert To Webex Sent'}
                else:
                    print(yellow('\n- You decided to directly isolate endpoint in ISE',bold=True))
                    result=quarantine_endpoint(infected_ip_address) # Query ISE pxgrid API to isolate endpoint
                    result = { 'status':'ISE Isolation Requested'}
            else:
                result = { 'status':'Dont isolate'}
            print("\nresult : ",yellow(result,bold=True))                 
            if result['status']=='FAILURE':
                print(red('- ERROR !',bold=True))
            else:
                print(green('- Ok Done - Now Check ISE ANC Policy Endpoint Assign',bold=True))
        if '<BAD IP ADDRESS>' in syslog:
            # we store the internal bad ip address into a file for the demo instead of querying ISE for hosts in sessions
            bad_ip_address=syslog.split(': ')[1]
            with open('./bad_ip.txt','w') as file:
                file.write(bad_ip_address)
                
if __name__=="__main__":
    print()
    print(env.level,white("MAIN FUNCTION ( the syslog server starts here ): >",bold=True))
    with open("./debug/log.txt","w") as file:
        pass
    loguer(env.level+" SYLOG SERVER STARTS")
    # set a default infected ip address
    with open('./bad_ip.txt','w') as file:
        file.write('0.0.0.0')    
    try:
        print('\n Let\'s start Syslog Server - listening on UDP 514')
        print(green(' All Good - listening on UDP 514 waiting for syslog messages',bold=True))
        server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)        
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")    
