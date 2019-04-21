import csv
import sys
import os
import datetime
from colorama import init, Fore, Back

#init changes

# Returns dictionary
def read_access_list():
    with open('access.csv', 'r') as accesslist:
        access = {}
        r = csv.reader(accesslist)
        # Create dictionary with site initial as key
        for li in r:
            access[li[0]] = {'emails': li[1], 'phones': li[2]} 
    accesslist.close()
    return access

def log(string, newline=False):
    if newline:
        line = [f'\n{str(datetime.datetime.now())} -- \t{string}']
    else:
        line = [f'{str(datetime.datetime.now())} -- \t{string}']

    with open(f'logs\\log.txt', 'a', newline="") as logfile:   
        writer = csv.writer(logfile)
        writer.writerow(line)
    logfile.close()

def write_csv(arr, file):
    with open(f'created\\{file}', 'w', newline='') as writefile:
        writer = csv.writer(writefile)
        writer.writerows(arr)
    writefile.close()
    print(f'{Fore.GREEN}Created {file}')
    log(f'Created {file}')
 
if __name__ == '__main__':
    # resets color every line
    init(autoreset=True)
    default_client = 'lc'

    if len(sys.argv) > 1:
        client = sys.argv[1]
    else:
        client = default_client

    log(f'Starting program. Client:{client}', True)

    allowed_sites = ['bb', 'dw', 'lf','ib','mrb','ws','lc','gl','sp','hw','rh','jp']
    if client in allowed_sites:
        # Access list as dictionary
        access = read_access_list()
        client_email = ""
        client_phone = ""
        access_status_colour = Fore.WHITE
        if client in access:
            client_email = access[client.lower()]["emails"].replace(";"," ")
            client_phone = access[client.lower()]["phones"].replace(";"," ")
        else:
            access_status_colour = Fore.RED
            print(f'{access_status_colour}There are no access details for a client with that initial')

        print(f'\n')

        
        file = f"vidraw-{client}.csv"
        print(f'Making files for {client}. \n\nRipping vehicles from {Fore.YELLOW}{os.getcwd()}\\{Fore.GREEN}{file}.')
        print(f'Access details: {access_status_colour}{client.upper()}\t{client_email}\t{client_phone}')
        log(f'Attempting to create files for {client.upper()} with acces: {client_email}\t{client_phone}')

        location = f'C:\\Website\\AusPost{client}\\mapper'
        predel_location = f'C:\\Website\\AusPostPreDelivery\\mapper'
        email = client_email
        predel_email = "photi@my-fleet.com"
        phone = client_phone
        predel_phone = ""
        vd_file = "vd.csv"
        shift_server = "mailserver2"
        timezone = 1

        vid_vehicles = []
        vid_predel = []
        esn = 'esn'.center(10)
        stat = 'status'.center(10)
        headers = f'{Back.YELLOW}{Fore.BLACK}\nCount\t{esn}\t{stat}'
        try:
            with open(file, mode="r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line = 0
                for row in csv_reader:
                    if line == 0:
                        print(headers)
                        line += 1
                        continue
                    
                    vid_vehicles.append([row[0], 'AusPost'+client, '1', row[0], '', location, '', email, phone, '','','','0','0','0','N', vd_file, 'N', shift_server, timezone])
                    vid_predel.append([row[0], 'AusPostPreDelivery', '1', row[0], '', predel_location, '', predel_email, predel_phone, '','','','0','0','0','N', vd_file, 'N', shift_server, timezone])

                    print(f'{line}:\t{row[0]}\t{Fore.GREEN}processed')
                    line += 1
                log(f'Processed {line-1} vehicles.')
            csv_file.close()

            log(f'Creating csv files.')
            newvid = f'vid-{client}.csv'
            newpredel = f'vid-predel-{client}.csv'
            write_csv(vid_vehicles, newvid)
            write_csv(vid_predel, newpredel)
        except:
            print(f'{Fore.RED}Could not find input file')
            log('Could not find input file.')

    else:
        print(f'{Fore.RED}There was no site matching that input argument.')
        log(f'There was no site matching that input argument.')

    print('Program finished.')
    log('Program finished')