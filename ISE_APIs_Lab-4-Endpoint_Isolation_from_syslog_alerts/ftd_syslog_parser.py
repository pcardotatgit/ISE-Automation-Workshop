# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : resources dedicated to parsing of FTD syslogs
'''
import env as env
from crayons import *
from analyse_application_logs import loguer

infected_machine_list=[]

#  def parse_ftd_single_log***
def parse_ftd_single_log(syslog):
    """
    MODIFIED : 2026-06-21T17:11:27.000Z

    description : parse FTD Log abd trigger some response actions
    
    how to call it :
    """
    route="/parse_ftd_single_log"
    env.level+="-"
    print("\n"+env.level,white("def parse_ftd_single_log() in ftd_syslog_parser.py : >\n",bold=True))
    loguer(env.level+" def parse_ftd_single_log() in ftd_syslog_parser.py : >")
    #print(green('\ndef parse_ftd_single_log() : >',bold=True))
    #print('syslog : \n',yellow(syslog,bold=True))
    log={}
    fields=syslog.split(',')
    #new_line=fields[0]+','+fields[4]+','+fields[5]+','+fields[6]+','+fields[7]+','+fields[8]+','+fields[13]+','+fields[17]+','+fields[18]+','+fields[19]+','+fields[20]
    #print(cyan(new_line,bold=True))
    timestamp=fields[0].split('  :')[0]
    timestamp=timestamp.split('>')[1]            
    DeviceUUID=fields[0].split(': ')[3]
    SrcIP=fields[4].split(': ')[1]
    DstIP=fields[5].split(': ')[1]
    SrcPort=fields[6].split(': ')[1]
    DstPort=fields[7].split(': ')[1]
    Protocol=fields[8].split(': ')[1]
    Priority=fields[13].split(': ')[1]
    Message=fields[17].split(': ')[1]
    Classification=fields[18].split(': ')[1]
    Client=fields[19].split(': ')[1]
    ApplicationProtocol=fields[20].split(': ')[1]
    log['timestamp']=timestamp
    log['DeviceUUID']=DeviceUUID
    log['SrcIP']=SrcIP
    log['DstIP']=DstIP
    log['SrcPort']=SrcPort
    log['DstPort']=DstPort
    log['Protocol']=Protocol
    log['Priority']=Priority           
    log['Message']=Message            
    log['Classification']=Classification
    log['Client']=Client
    log['ApplicationProtocol']=ApplicationProtocol
    print(yellow('\n< IPS ALERT !!! >\n',bold=True), timestamp,' From ',red(SrcIP,bold=True),' to => ',cyan(DstIP,bold=True),'\n','Message : '+yellow(Message,bold=True),'\n','Priority : '+Priority+'\n\n')
    #print(yellow(log,bold=True))
    if SrcIP not in infected_machine_list:
        infected_machine_list.append(SrcIP)
        print('\n==============\nNew Infected List : ',yellow(infected_machine_list,bold=True),'\n==============\n')
    env.level=env.level[:-1]        
    return(log)



