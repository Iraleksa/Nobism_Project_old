import requests.exceptions
import json
import pandas as pd
import re

def token():
#    choice = []
#    question = 'Token : '
#    sys.stdout.write(question)
#    choice = input(), choice
#    global access_token

    access_token = "WQvJlgPSMDnkPHWfsbMorb2qHSYvW4ohbh7KOVidcwMHspmMYVDDd3mgxMWcJUIh" #choice[0]
    url = "https://www.openhumans.org/api/direct-sharing/project/members/?access_token="
    url_data = url + str(access_token)
    try:
        r = requests.get(url_data)
        r.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("Connection with Open Human is Down")
    except requests.exceptions.HTTPError:
        print("Connection with Open Human fail")
    else:
        print("Connected to open human")  # Proceed to do stuff with `r`


    Data = json.loads(r.text)
    return Data


def store_all_data(Data):
    import pandas as pd

    Global_Data = pd.DataFrame()

    for user in Data['results']:

        data = pd.DataFrame()
        
        if user['project_member_id'] == "36057926":  #getting data from user 36 only
        
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
        Global_Data.to_csv("../data/ML.csv")


store_all_data(token())


def Tag():
    Tag = pd.read_csv('../data/Tag.csv')
    Data = pd.read_csv('../data/ML.csv')

    
    for index, row in Data.iterrows():
        try:
            row["Tag"] = re.sub(r"^.+-", "", str(row["Tag"]))
            x = re.sub(r".{2}$", "", str(row["Tag"]))
            Data.set_value(index,'Tag', x)
            x = Tag["code"].loc[Tag["code"] == row["Tag"]].index
            Data.loc[index, "Name"] = Tag.iloc[x[0]]["English"]
            
        except:
            pass
        
    
    Data.to_csv("../data/machine-learning_user36.csv")
Tag()