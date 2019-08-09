#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Imports and Settings
import sys

for path in sys.path:
    print(path)
# Set path directory
import sys, os
sys.path.append(os.path.realpath(".."))
import datetime
import pandas as pd
import plotnine as p9
# Get the time now
current_time = datetime.datetime.now()

# Connect to Open Human
# REFRESH  access_token if needed
access_token = "jiZRwcgP63E3AqoNmV7kTEedLRpQnmn3mKZh2PR4j3EM4w9JJHwtxxQBk3R3gIjM"
def token(access_token):
    import requests.exceptions
    import json
    #choice = []
    #question = 'Token : '
    #sys.stdout.write(question)
    #choice = input(), choice
    #access_token = choice[0]
    #global access_token
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
        print("Connected to open human")

    Data = json.loads(r.text)
    return Data

Data_oh = token(access_token)

print("======================")
print(len(Data_oh['results']), "users are registered")
print("======================")
type
# Store Data as file
from functions2 import open_human
from functions2 import preprocessing
from functions2 import clean
from functions2 import code
from functions2 import graph
import os
import subprocess
current_path = os.getcwd()

for user in Data_oh['results']:
    global name
    name = user['project_member_id']

    # Get the data from open human REVIEW###################################
    if open_human.get_data(user) == 0:
        
        cmd = ['mkdir', current_path + '/pdf/Final/' + name]
        subprocess.call(cmd)
        print("Folder" + name + "created")
        # save it as .csv in ../data
        Data = preprocessing.load()
        print('Load OK`')
        # create folder for user
        preprocessing.create_folder(name)
        print('Folder OK')
        #preprocess na's
        Data = Data.dropna(thresh = 7)
        print("Full na's rows removed")
        # preprocess Tag
        Data = preprocessing.Tag(Data)
        print('Preprocess tag OK')
        # preprocess Data time
        Data = preprocessing.DateTime(Data)
        print('Preprocess datetime OK')
        # preprocess Intensity
        Data = preprocessing.Intensity(Data)
        print('Preprocess Intensity OK')
        # Duration
        Data = preprocessing.duration(Data)
        print('Preprocess Duration OK')
        # split Data
        Data_m = preprocessing.Split_data(Data, current_time.day, 
                                          current_time.month, 
                                          current_time.year)
        print('Preprocess Split OK')
        # Build Json
        LISTE = code.Json(Data, Data_m)
        print('Json OK')
        # Build Graphs
        graph.TL_1(Data)
        graph.TL_2(Data)
        graph.TL_3(Data)
        graph.TL_4(Data)
        graph.graph_1(Data,Data_m)
        graph.graph_2(Data,Data_m)
        graph.graph_3(Data,Data_m)
        graph.medicine(Data)
        print('Preprocess Graphs and TimeLines OK') 
        #Plot's images not found?
        code.img_not_found()
        # Load Json
        code.json_file()
        print('json_file OK')
        #Build HTML
        code.upload_html()
        print('html upload OK')
        # Convert into PDF
        code.convert_into_pdf(name)
        print('PDF OK')
        # Clean Data
        cmd = ['cp', current_path + '/data/main.csv', 
               current_path + '/pdf/Final/' + name + '/']
        subprocess.call(cmd, universal_newlines=True)
        clean.clean_data()
        print('Clean data OK')

#import xhtml2pdf.pisa as pisa
# Clean PDF
clean.rm_folders()

# Build Metadata
code.metadata_build()

# Sent PDF
security = " " # security is the Token we are using to load the data
open_human.metadata_send(access_token)
