ip_address=input('Enter an IP address : ')

with open('./syslogs_template.txt') as file:
    text_content=file.read()
    
new_content=text_content.replace('SrcIP: 192.168.95.7','SrcIP: '+ip_address)

with open('./syslogs.txt','w') as file:
    file.write(new_content)
    
with open('./bad_ip.txt','w') as file:
    file.write(ip_address)
    
print('OK DONE the syslogs.txt file was created')