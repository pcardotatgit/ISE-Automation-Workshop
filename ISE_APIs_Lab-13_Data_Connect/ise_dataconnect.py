# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : ISE Dataconnect API Lab
'''
import env as env
from crayons import *
from analyse_application_logs import loguer
import traceback
import argparse
import csv
import json
import logging
import oracledb
import os
import signal
import ssl
import sys
import tabulate
import time
import yaml

FORMATS = ["csv", "grid", "json", "line", "markdown", "pretty", "yaml", "table", "text"]

# def_parse_config_to_dict***
def parse_config_to_dict(config_json_file):
    '''
        version : 2026-03-05
        
        description : read the file input thru config_json_file and create a dictionnary that contains key names and their value from the json input
    '''
    env.level+='-'
    print(env.level,white('def parse_config_to_dict() in ise_dataconnect.py  : >\n',bold=True))
    loguer(env.level+' def parse_config_to_dict() in ise_dataconnect.py  : > ')
    with open(config_json_file, 'r') as f:
        conf_result=json.load(f)   
    print(green(conf_result,bold=True))
    env.level=env.level[:-1]
    return conf_result



#  def main***
def main():
    """
    MODIFIED : 2026-10-23T09:43:18.000Z

    description : main function
    
    how to call it : main()
    """
    env.level+='-'
    print(env.level,white('def main() in ise_dataconnect.py  : >\n',bold=True))
    loguer(env.level+' def main() in ise_dataconnect.py  : > ')
    app_config=parse_config_to_dict('./config.json')
    hostname=app_config['hostname']
    password=app_config['password']
    print("\nhostname : ",hostname) 
    print("\npassword : ",password)
    #a=input('Next ...')
    #insecure = args.insecure or os.environ.get("ISE_VERIFY", "True")[0:1].lower() in ["f", "n"]
    selected_query='./SQL_queries/'+select_sql_query()
    print(' Selected query PATH is :',cyan(selected_query,bold=True))
    a=input('Press ENTER...')
    insecure = 1 # for lab only

    if hostname is None:
        sys.exit("Missing hostname: Set ISE_PMNT environment variable or use --hostname option")
    if password is None:
        sys.exit("Missing password: Set ISE_DC_PASSWORD environment variable or use --password option")

    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context = ssl.create_default_context()
    if insecure:
        ssl_context.check_hostname = False  # required before setting verify_mode == ssl.CERT_NONE
        ssl_context.verify_mode = ssl.CERT_NONE  # any cert is accepted; validation errors are ignored
    log.debug(f"{'⚠🔓' if insecure else '✔🔒'} TLS security {'dis' if insecure else 'en'}abled")

    ISE_DC_PORT = 2484  # Data Connect port
    ISE_DC_SID = "cpm10"  # Data Connect service name identifier
    ISE_DC_USERNAME = "dataconnect"  # Data Connect username

    params = oracledb.ConnectParams(
        protocol="tcps",  # tcp "secure" with TLS
        host=hostname,  # hostname or IP address of database host machine
        port=ISE_DC_PORT,  # Oracle Default: 1521
        service_name=ISE_DC_SID,
        user=ISE_DC_USERNAME,
        password=password,
        retry_count=3,  # connection attempts retries before being terminated. Default: 0
        retry_delay=3,  # seconds to wait before a new connection attempt. Default: 0
        ssl_context=ssl_context,  # an SSLContext object which is used for connecting to the database using TLS
        ssl_server_dn_match=False,  # boolean indicating if the server certificate distinguished name (DN) should be matched. Default: True
        # ssl_server_cert_dn=False # the distinguished name (DN), which should be matched with the server
        # wallet_location=DIR_EWALLET, # the directory containing the PEM-encoded wallet file, ewallet.pem
    )
    log.debug(f"OracleDB Connection String: {params.get_connect_string()}")

    try:
        with oracledb.connect(params=params) as connection:
            with connection.cursor() as cursor:

                # load SQL query from file?
                query = read_sql_file(selected_query)

                log.debug(f"SQL query:\n-----\n{query}\n-----")
                cursor.execute(query)
                '''  WE KEEP THIS FROM THE ORIGINAL iseqls.py as reference
                # Use CSV by default to stream results without large memory buffering
                if args.format == "csv":
                    # Get header names from cursor.description, a list of sets about each column:
                    #   [ (name, type_code, display_size, internal_size, precision, scale, null_ok), ... ]
                    headers = [f"{i[0]}".lower() for i in cursor.description]
                    writer = csv.writer(sys.stdout, quoting=0, skipinitialspace=True)
                    writer.writerow(headers)
                    while True:
                        rows = cursor.fetchmany()  # use default Cursor.arraysize
                        if not rows:
                            break
                        #writer.writerows(rows)         
                        lines_out=''                        
                        for row in rows:
                            print(yellow(row,bold=True))
                            lines_out=lines_out+json.dumps(row)+'\n'
                            #print(red(text_out,bold=True))
                        print(lines_out)
                    # SAVE RESULTS HERE UNDER
                    with open('./result/result.txt','w') as file:
                        file.write(lines_out)
                else:
                    # All other formats require buffering all results in memory for column width sizing (grid|table) or map attribute names (JSON|YAML)
                    headers = [f"{i[0]}".lower() for i in cursor.description]
                    rows = cursor.fetchall()  # returns a list of tuples
                    show(table=rows, headers=headers, format=args.format)
                '''
                headers = [f"{i[0]}".lower() for i in cursor.description]
                rows = cursor.fetchall()  # returns a list of tuples
                show(table=rows, headers=headers, format="json")
    except oracledb.Error as e:
        log.error(f"Oracle Error: {e}")
    except Exception as e:
        log.error(f"Error: {e}")
    env.level=env.level[:-1]
    return 1

#  def show***
def show(table: list = None, headers: list = None, format: str = "text", filepath: str = "-") -> None:
    '''
    MODIFIED : 2026-10-23T09:45:55.000Z

    description : rint the table in the specified format to the file. Default: `sys.stdout` ('-').
    
    BUT IT Was package only for JSON ouput !
    
    for reference original options
    
    - table (list) : a list of list items to show
    - headers (list) : the column names for the table
    - format (str): one the following formats:
      - `csv`   : Show the items in a Comma-Separated Value (CSV) format
      - `grid`  : Show the items in a table grid with borders
      - `json`  : Show the items as a single JSON string
      - `line`  : Show the items each on their own line in JSON format
      - `markdown`: Show the items in Markdown format
      - `pretty`: Show the items in an indented JSON format
      - `table` : Show the items in a text-based table
      - `text`  : Show the items in a text-based table (no header line separator)
      - `yaml`  : Show the items in a YAML format
    - filepath (str) : Default: `sys.stdout`    
    
    OUTPUT : this function creates ./result/result.json
    
    how to call it : show(table=rows, headers=headers, format="json")
    '''
    env.level+='-'
    print(env.level,white('def show() in ise_dataconnect.py  : >\n',bold=True))
    loguer(env.level+' def show() in ise_dataconnect.py  : > ')
    if table == None or len(table) <= 0:
        return

    # 💡 Do not close sys.stdout or it may not be re-opened with multiple show() calls
    fh = sys.stdout if filepath == "-" else open(filepath, "w")  # write to sys.stdout/terminal by default

    if format == "csv":  # CSV
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(table)
    elif format == "grid":  # grid
        print(f"{tabulate.tabulate(table, headers=headers, tablefmt='simple_grid')}", file=fh)
    elif format == "table":  # table
        print(f"{tabulate.tabulate(table, headers=headers, tablefmt='table')}", file=fh)
    elif format == "json":  # JSON, one long string
        #print(json.dumps({"table": [dict(zip(headers, row)) for row in table]}, default=(lambda o: str(o))), file=fh)
        texte=json.dumps({"table": [dict(zip(headers, row)) for row in table]}, default=(lambda o: str(o)),sort_keys=True,indent=4, separators=(",", ": "))
        print(cyan(texte,bold=True))
        # SAVE RESULTS HERE UNDER
        with open('./result/result.json','w') as file:
            file.write(texte)
    elif format == "line":  # 1 JSON object per line
        print("{", file=fh)
        print(f'"table" : [', file=fh)
        print(",\n".join([json.dumps(r, default=(lambda o: str(o))) for r in [dict(zip(headers, row)) for row in table]]), file=fh)
        print("]\n}", file=fh)
    elif format == "markdown":
        print(f"{tabulate.tabulate(table, headers=headers, tablefmt='github')}", file=fh)
    elif format == "pretty":  # pretty-print with 2-space indents
        print(json.dumps({"table": [dict(zip(headers, row)) for row in table]}, default=(lambda o: str(o)), indent=2), file=fh)
    elif format == "yaml":  # YAML
        print(yaml.dump({"table": [dict(zip(headers, row)) for row in table]}, indent=2, default_flow_style=False), file=fh)
    elif format == "text":  # pretty-print
        print(f"{tabulate.tabulate(table, headers=headers, tablefmt='plain')}", file=fh)
    else:  # just in case something gets through the CLI parser
        log.error(f"Unknown format: {format}")
    env.level=env.level[:-1]
    return 1

#  def read_sql_file***
def read_sql_file(filepath: str = None) -> str:
    '''
    MODIFIED : 2026-10-23T09:49:36.000Z

    description :     Read and return the file contents at the filepath.
                        filepath (str) : an absolute or relative path from this script.
                        returns (str) : the file contents as a string.
    
    how to call it : query = read_sql_file(args.query)
    '''
    env.level+='-'
    print(env.level,white('def read_sql_file() in ise_dataconnect.py  : >\n',bold=True))
    loguer(env.level+' def read_sql_file() in ise_dataconnect.py  : > ')
    log.debug(f"filepath={filepath}")
    assert filepath.strip().lower().endswith(".sql")
    assert os.path.exists(filepath)
    assert os.path.isfile(filepath)
    env.level=env.level[:-1]
    with open(filepath, mode="r", encoding="utf-8") as fh:
        return fh.read()
#  def select_sql_query***
def select_sql_query():
    """
    MODIFIED : 2026-10-23T10:02:15.000Z

    description : list all available sql queries and select one to use
    
    how to call it :
    """
    route="/select_sql_query"
    env.level+="-"
    print("\n"+env.level,white("def select_sql_query() in ise_dataconnect.py : >\n",bold=True))
    loguer(env.level+" def select_sql_query() in ise_dataconnect.py : >")
    # ===================================================================    
    file_dict=list_files_in_dir('./SQL_queries','.sql')
    text_result=json.dumps(file_dict,sort_keys=True,indent=4, separators=(",", ": "))
    print("\nfile_dict : ",yellow(text_result,bold=True)) 
    index=0
    file_list=[]
    for fichier in file_dict[0]:
        file_list.append(fichier)
        print(yellow('Index = '+str(index),bold=True),fichier)
        index+=1
    selection=input('Select one query index : ')
    selected_index =int(selection)
    selected_query=file_list[selected_index]
    print(' Selected query is :',cyan(file_list[selected_index],bold=True))
    # ===================================================================
    #loguer(env.level+" def END OF select_sql_query() in ise_dataconnect.py : >")    
    env.level=env.level[:-1]
    return selected_query

#  def list_files_in_dir***
def list_files_in_dir(directory,file_type):
    '''
    MODIFIED : 2026-08-03T09:28:31.000Z

    description : list files in the selected directory
    
    how to call it : file_dict=list_files_in_dir(directory,file_types)
        directory= ex: ./subdir or c:/full_path/
        file_types = extension ex .py, .txt, .doc etc
    returns :
        file_dict=dictionnary
        index=number of found files
    '''
    route="/list_files_in_dir"
    env.level+="-"
    print("\n"+env.level,white("def list_files_in_dir() in ise_dataconnect.py : >\n",bold=True))
    loguer(env.level+" def list_files_in_dir() in ise_dataconnect.py  : > ")
    # ===================================================================    
    files =[file for file in os.listdir(directory)] 
    file_dict={}
    index=0
    for file in files:
        if  file_type in file:
            print(' file : ',yellow(file,bold=True))
            file_dict[file]={'name':file}
            index+=1
    # ===================================================================
    #loguer(env.level+" def END OF list_files_in_dir() in ise_dataconnect.py  : > ')
    env.level=env.level[:-1]
    return file_dict,index


if __name__=="__main__":
    print(env.level,white("MAIN FUNCTION ( the application starts here ): >",bold=True))
    with open("./debug/log.txt","w") as file:
        pass
    loguer(env.level+" APPLICATION STARTS")
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))  # Handle CTRL+C interrupts gracefully

    start_time = time.time()

    # Create a default logger to sys.stderr
    logging.basicConfig(
        stream=sys.stderr,
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(module)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log = logging.getLogger()
    log.setLevel("WARNING")  # logging threshold

    main()

    print(green('\nOK DONE Results are in [ ./result/result.json ] file',bold=True))
