
def world():
    print("Hello World")

import requests.exceptions
import json
import sys

#def token():
#    import requests.exceptions
##    choice = []
##    question = 'Token : '
##    sys.stdout.write(question)
##    choice = input(), choice
##    global access_token
##
#   # access_token = choice[0]
#    url = "https://www.openhumans.org/api/direct-sharing/project/members/?access_token="
#    url_data = url + str(access_token)
#    try:
#        r = requests.get(url_data)
#        r.raise_for_status()
#    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
#        print("Connection with Open Human is Down")
#    except requests.exceptions.HTTPError:
#        print("Connection with Open Human fail")
#    else:
#        print("Connected to open human")  # Proceed to do stuff with `r`
#
#    Data = json.loads(r.text)
#    return Data

import pandas as pd

def get_data(user):

    # Creat DATA dataframe who will receive all data from the user
    DATA = pd.DataFrame()

    # Iterate amonge the key to found Symptoms.csv
    for x in range(0, len(user['data'])):

        # Loop for a specific file
        if user['data'][x]['basename'] == 'Symptoms.csv':

            #Get the url from where we can download the data
            download_url = user['data'][x]['download_url']

            # Import data into n, a dataframe
            n = pd.read_csv(download_url, error_bad_lines=False)

            # Merge n with DATA in case there is more than one Symptoms.csv
            frames = [DATA, n]
            DATA = pd.concat(frames, sort=True)

    # Return Data OK
    if len(DATA) > 1:

        # Save data into folder as csv
        DATA.to_csv("data/main.csv")

        print('=========',user['project_member_id'], "has", len(DATA), "rows",'=========')
        return (0)

    # Return no Data
    else:
        return (1)




def store_all_data(Data):
    import pandas as pd

    Global_Data = pd.DataFrame()

    for user in Data['results']:

        data = pd.DataFrame()

        for x in range(0, len(user['data'])):

            if user['data'][x]['basename'] == 'Symptoms.csv':

                download_url = user['data'][x]['download_url']

                n = pd.read_csv(download_url, error_bad_lines=False)

                frames = [data, n]
                data = pd.concat(frames, sort=True)

        if len(data) > 1:
            frames = [Global_Data , data]
            Global_Data = pd.concat(frames, sort=True)

    print(len(Global_Data))

import subprocess

def metadata_send(security):
    cmd = ['ohproj-upload', '-T', security, '--metadata-csv',
           'metadata.csv', '-d', 'PDF']

    subprocess.call(cmd, universal_newlines=True)

    print("Data sent !")
