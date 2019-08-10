#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 12:44:44 2019

@author: valerian
"""

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
    Global_Data.to_csv("../Code/data/ML.csv")


store_all_data(token())

### TAG

Tag = pd.read_csv('../Code/data/Tag.csv')
Data = pd.read_csv('../Code/data/ML.csv')


for index, row in Data.iterrows():
    try:
        row["Tag"] = re.sub(r"^.+-", "", str(row["Tag"]))
        x = re.sub(r".{2}$", "", str(row["Tag"]))
        Data.set_value(index,'Tag', x)
        x = Tag["code"].loc[Tag["code"] == row["Tag"]].index
        Data.loc[index, "Name"] = Tag.iloc[x[0]]["English"]

    except:
        pass

Data.to_csv("../Code/data/ML.csv")

#### DATE

from datetime import datetime

df = pd.read_csv('../Code/data/ML.csv')

for index, row in df.iterrows():
    try:
        row["Date/Time"] = row["Date/Time"].lstrip()
        row["Date/Time"] = row["Date/Time"][:16]
        row["Date/Time"] = datetime.datetime.strptime(row["Date/Time"], '%d/%m/%Y %H:%M')
    except:
        pass

df['date'] = pd.to_datetime(df["Date/Time"])
df['year'], df['month'], df["day"], df["hour"] = df['date'].dt.year, df['date'].dt.month, df['date'].dt.day, df['date'].dt.hour
df.to_csv("../Code/data/ML.csv")

### INTENSITY

df = pd.read_csv('../Code/data/ML.csv')
df['Intensity'] = pd.to_numeric(df['Intensity'], errors='coerce')
df.to_csv("../Code/data/ML.csv")

### DURATION

df = pd.read_csv('../Code/data/ML.csv')
df['Duration'] =  pd.to_datetime(df['Duration'], format='%H:%M:%S', errors='coerce').dt.time
df['Duration'] = df['Duration'].apply(lambda x: (x.hour * 60 + x.minute))
df.to_csv("../Code/data/ML.csv")