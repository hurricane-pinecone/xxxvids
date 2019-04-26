# james.couch@my-fleet.com
# Last change 24/04/2019

import csv
import sys
import os
import datetime
from colorama import init, Fore, Back

from xxxvids_func import *


##  Main Program
##  
##
##

if __name__ == '__main__':
    # resets color every line
    Fore.YELLOW
    init(autoreset=True)
    Fore.YELLOW

    # client-initial: vid row as string
    dict_client_db = {}
     # Access list as dictionary
    access_csv = 'access.csv'
    access = read_access_list(access_csv)

    try:
        dict_config, client = read_config()
        client_config = {'config': dict_config[client]}
        dict_client_db.update({client: client_config})

        conf = dict_client_db[client]['config']
        print(f'{Fore.YELLOW}Preparing to generate csv with config: {Fore.CYAN}{conf}')
        #print(dict_config_data)
    except:
        err = f'Something went wrong reading config file'
        print(err)
        log(err)

    for i, client in enumerate(dict_client_db):
        key = {'emails': access[client]['emails'], 'phone': access[client]['phones']}
        dict_client_db[client].update({'access': key})

        client_access = dict_client_db[client]['access']
        print(f'{Fore.YELLOW}Preparing to generate vid with access: {Fore.CYAN}{client_access}')
        vid = generate_vid(dict_client_db, access, client)
        dict_client_db[client].update(vid)


    print('Program finished.')
    log('Program finished')