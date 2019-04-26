# Returns dictionary
import csv
import datetime
from colorama import init, Fore, Back
import sys

def read_access_list(access = "access.csv"):
    """Return access dictionary from csv file"""
    print(f'Reading telematics acces list...\t{access}')
    with open("access.csv", 'r') as accesslist:
        access = {}
        r = csv.reader(accesslist)
        # Create dictionary with site initial as key
        for li in r:
            access[li[0]] = {'emails': li[1], 'phones': li[2]} 
    return access

# return dictionary of client config
def read_config(config_file = 'config.csv'):
    """Reads in variables from config.csv"""
    print(f'Reading config file...\t\t\t{config_file}')
    dict_config = {}
    config = []
    with open(config_file, 'r') as configf:
        configraw = csv.reader(configf, delimiter='\n')

        for li in configraw:
            config.append(li)

    client              = ''
    division            = ''
    location            = ''
    myfleet_email       = ''
    vd_file             = ''
    shift_server        = ''
    timezone            = 0

    config_len = len(config_file)
    start = 7       # Allows for comment section at top of csv
    inc = 7
    clients = 0

    for i in range (start, config_len, inc):
        client = ''.join(config[i]) 

        division        = ''.join(config[i + 1])
        location        = ''.join(config[i + 2])
        myfleet_email   = ''.join(config[i + 3])
        vd_file         = ''.join(config[i + 4])
        shift_server    = ''.join(config[i + 5])
        timezone        = ''.join(config[i + 6])

        dict_config =   {client: {'division': division,
                        'location': location,
                        'myfleet-email': myfleet_email,
                        'vd-file': vd_file,
                        'shift-server': shift_server,
                        'timezone': timezone}}

    Fore.WHITE
    return dict_config, client


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
    Fore.WHITE

def write_csv(arr, file):
    with open(f'created\\{file}', 'w', newline='') as writefile:
        writer = csv.writer(writefile)
        writer.writerows(arr)
    print(f'{Fore.GREEN}Created {file}')
    log(f'Created {file}')
    Fore.WHITE

def generate_vid(db, access, client):
    div = db[client]['config']['division']

    vid = []
    vid_predel = []

    config = {}
    config = db[client]['config']
    location = config['location']
    mfe = db[client]['config']['myfleet-email']
    acc = access[client]['emails']
    myfleet_email = config['myfleet-email']
    client_email = access[client]['emails']
    email = f'{mfe};{acc}'
    phone = access[client]['phones']
    vd_file = config['vd-file']
    shift_server = config['shift-server']
    timezone = config['timezone']
    predel_location     = f'C:\\Website\\AusPostLC\\mapper'

    print(f'\nConcatenating myfleet emails\t\t{myfleet_email}\t\t{client_email}\t\t=> {Fore.GREEN}{email}')
    print(f'{Fore.GREEN}GENERATING VID FOR {client.upper()}-{div}')

    # Write vid file from input csv
    for i, client in enumerate(db):
        file = f"input-{client}.csv"
        try:
            with open(file, 'r') as csv_file:     
                Fore.YELLOW
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
                
                log(f'Processed {i-1} vehicles.')

            log(f'Creating csv files.')
            newvid = f'vid-{client}.csv'
            newpredel = f'vid-predel-{client}.csv'
            write_csv(vid, newvid)
            write_csv(vid_predel, newpredel)
        except IOError:
            type, value, traceback = sys.exc_info()
            err = f'{Fore.RED}Could not find input file {file} {type} {value} {traceback}'
            print(err)
            log(err)    
    print('vids created')

    vidkey = {'vid': vid}

    Fore.WHITE

    return vidkey