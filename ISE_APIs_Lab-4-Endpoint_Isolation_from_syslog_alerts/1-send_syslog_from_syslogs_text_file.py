#!/usr/bin/python
# -*- encoding: iso-8859-1 -*-
import socket
import time

syslog_server_ip='localhost'

def send_syslogs(message,syslog_server_ip):
    host=syslog_server_ip
    port=514
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect((host,port))
    b = bytes(message, 'utf-8')
    s.sendall(b)
    s.close()

if __name__=='__main__':
    print(f'let\'s send syslog messages to {syslog_server_ip} \n')
    with open('syslogs.txt') as file:
        txt_content=file.read()
    lines=txt_content.split('\n')
    for line in lines:
        line=line.strip()
        if line!='':
            print(line)
            send_syslogs(line,syslog_server_ip)
            #time.sleep(1)
    print('\nOK ALL DONE\n')
    