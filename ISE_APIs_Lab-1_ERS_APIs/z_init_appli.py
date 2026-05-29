'''
    modification : 20260315
    
    description : initialize the application, create empty files  clean folder, reset folders
'''
import glob
import os
#from crayons import *

def create_structure():
    # example to customize
    os.mkdir("./debug")
    os.mkdir("./result")
    os.mkdir("./observables ")      
    os.mkdir("./keys")     
    with open("./keys/config.txt",'w') as file:
        outlines='''{
profil_name=XDR Tenant name
ctr_client_id=client-0932888d-xxxx
ctr_client_password=RMllP4-xxx
host=https://private.intel.eu.amp.cisco.com
host_for_token=https://visibility.eu.amp.cisco.com
}
        '''
        file.write(outlines)   


def init_appli():
    '''
    with open('./venv/Scripts/activate.bat') as file:
        text_content=file.read()
    text_content=text_content.replace(':END','python convert.py\n:END')
    with open('./venv/Scripts/activate.bat','w') as file:
        file.write(text_content)    
    '''
    os.remove("a.bat")
    os.remove("b.bat")
    os.remove("c.bat")
    os.remove("d.bat") 
    #os.remove("e.bat")
    with open('a.bat','w') as file:
        file.write('venv\\scripts\\activate')    
    with open('b.bat','w') as file:
        file.write('python z.py') 

        
if __name__=="__main__":
    #create_structure()
    init_appli()    
    print('OK DONE')