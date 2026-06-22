'''
    modification : 20260315
    
    description : initialize the application, create empty files  clean folder, reset folders
'''
import glob
import os
#from crayons import *



def init_appli():
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