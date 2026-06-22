import sys
import sqlite3
import requests
import env as env
from crayons import *
from analyse_application_logs import *

#  def_read_db***
def read_db(database,table,where_clause):
    """
    MODIFIED : 2025-11-29T17:46:12.000Z

    description : Read entry from the selected database
    
    how to call it : entry_list=read_db(database,table,where_clause)
    
    """
    route="/read_db"
    env.level+="-"
    print("\n"+env.level,white("def read_db() in app.py : >\n",bold=True))
    loguer(env.level+" def read_db() in app.py : >")
    # ===================================================================    
    liste=[]
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        sql_request = f"SELECT * from {table} {where_clause}"
        print("\n sql_request in read_db() -> ",sql_request)
        print()
        try:
            cursor.execute(sql_request)
            for resultat in cursor:
                print("resultat : ",resultat)
                liste.append(resultat)
        except:
            sys.exit("couldnt read database")
    print("resultat list : ",liste)
    # ===================================================================
    #loguer(env.level+" def END OF read_db() in app.py : >")    
    env.level=env.level[:-1]
    return(liste)

#  def_read_variable_from_variable_db***
def read_variable_from_variable_db(variable):
    """
    MODIFIED : 2026-02-26
    description : read the value of passed variable name and return it ... to assign the an output variable
    
    how to call it : resultat=read_variable_from_variable_db(variable)
    """
    route="/read_variable_from_variable_db"
    env.level+="-"
    print("\n"+env.level,white("def read_variable_from_variable_db() in app.py : >\n",bold=True))
    loguer(env.level+" def read_variable_from_variable_db() in app.py : >")  
    print ("variable name :",yellow(variable,bold=True))
    database = os.getcwd()+"/../../../z_bases/variables.db"
    database=database.replace("\\","/")
    table="variables"
    print("database is :",database)    
    print("table is :",table)  
    where_clause=" where name='"+variable+"'"
    variable=""    
    variable_out=read_db(database,table,where_clause)
    print("-->> found entry ind DB :\n",variable_out)    
    if variable_out=="" or variable_out==[]:
        variable="no_value"
        print("\nvariable_out : ",red(variable_out,bold=True))
    else:
        variable=variable_out[0][3]
    env.level=env.level[:-1]
    return variable

    