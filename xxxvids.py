# james.couch@my-fleet.com
# Last change 24/04/2019

import csv
import sys
import os
import datetime
from colorama import init, Fore, Back

# Returns dictionary
def read_access_list():
    """Return access dictionary from csv file"""
    with open('access.csv', 'r') as accesslist:
        access = {}
        r = csv.reader(accesslist)
        # Create dictionary with site initial as key
        for li in r:
            access[li[0]] = {'emails': li[1], 'phones': li[2]} 
    return access

def read_config(config_file = 'config.csv'):
    """Reads in variables from config.csv"""
    config = []
    with open(config_file, 'r') as configf:
        configraw = csv.reader(configf, delimiter='\n')
        for li in configraw:
            config.append(li)
    return config


def log(string, newline=False):
    now = datetime.datetime.now()
    time = now.strftime("%a %d %m %Y")
    if newline:
        line = [f'\n{time} -- \t{string}']
    else:
        line = [f'{time} -- \t{string}']

    with open(f'logs\\log.txt', 'a', newline="") as logfile:   
        writer = csv.writer(logfile)
        writer.writerow(line)

def write_csv(arr, file):
    with open(f'created\\{file}', 'w', newline='') as writefile:
        writer = csv.writer(writefile)
        writer.writerows(arr)
    print(f'{Fore.GREEN}Created {file}')
    log(f'Created {file}')


##  Main Program
##  
##
##

if __name__ == '__main__':
    # resets color every line
    init(autoreset=True)

    ### Dictionary [LC] [vid]

    # client-initial: vid row as string
    vid = []
    vid_predel = []
    dict_client_db = {} 

    client              = ''
    location            = ''
    myfleet_email       = ''
    vd_file             = ''
    shift_server        = ''
    timezone            = 0
    predel_location     = f'C:\\Website\\AusPostLC\\mapper'

    try:
        config_data = read_config()
    except IOError:
        err = f'Something went wrong trying to open Config.csv'
        print(err)
        log(err)

     # Access list as dictionary
    access = read_access_list()
    
    config_len = len(config_data)
    start = 6       # Allows for comment section at top of csv
    clients = 0
    for i in range(start, config_len, 6): 
        client = ''.join(config_data[i])

        client_email = ""
        client_phone = ""
        access_status_colour = Fore.WHITE
        if client in access:
            client_email = access[client.lower()]["emails"]
            client_phone = access[client.lower()]["phones"]
        else:
            access_status_colour = Fore.RED
            print(f'{access_status_colour}There are no access details for a client with that initial')
        
        location        = ''.join(config_data[i + 1])
        myfleet_email   = ''.join(config_data[i + 2])
        email           = myfleet_email + ';' + client_email
        phone           = client_phone
        vd_file         = ''.join(config_data[i+3])
        shift_server    = ''.join(config_data[i+4])
        timezone        = ''.join(config_data[i+5])

        key = {client: 'vid'}
        dict_client_db.update(key)

        print('Reading config\n', '\n'.join([client, location, myfleet_email, vd_file, shift_server, timezone]))
        print(f'\nConcatenating myfleet emails\t\t{myfleet_email}\t\t{client_email}\t\t=> {Fore.GREEN}{email}')
        print('Printing vid file')

        # Write vid file from input csv
        for i, client in enumerate(dict_client_db):
            file = f"input-{client}.csv"
            try:
                with open(file, 'r') as csv_file:     
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for i, row in enumerate(csv_reader, start=0):
                        # Writes respective vids
                        line = ''
                        predel_line = ''
                        line        = [row[0], 'AusPost'+client, '1', row[0], '', location, '', email, phone, '','','','0','0','0','N', vd_file, 'N', shift_server, timezone]
                        predel_line = [row[0], 'AusPostPreDelivery', '1', row[0], '', predel_location, '', myfleet_email, '', '','','','0','0','0','N', vd_file, 'N', shift_server, timezone]
                        vid.append          (line)
                        vid_predel.append   (predel_line)

                        print(f'{i}:\t{line}\t{Fore.GREEN}processed')
                    
                    dict_client_db[client] = {'vid': vid}
                    log(f'Processed {i-1} vehicles.')

                log(f'Creating csv files.')
                newvid = f'vid-{client}.csv'
                newpredel = f'vid-predel-{client}.csv'
                write_csv(dict_client_db[client]['vid'], newvid)
                write_csv(vid_predel, newpredel)
            except IOError:
                type, value, traceback = sys.exc_info()
                err = f'{Fore.RED}Could not find input file {file} {type} {value} {traceback}'
                print(err)
                log(err)

        print('\n')


    print('Program finished.')
    log('Program finished')