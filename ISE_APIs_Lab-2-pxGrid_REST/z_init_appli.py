'''
    modification : 20260315
    
    description : initialize the application, create empty files  clean folder, reset folders
'''
import glob
import os
#from crayons import *


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
        
if __name__=="__main__":
    #create_structure()
    init_appli()    
    print('OK DONE')