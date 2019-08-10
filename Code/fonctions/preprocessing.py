#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:00:44 2019

@author: valerian
"""


import pandas as pd

def load():
    Data = pd.read_csv('data/main.csv')
    return(Data)

import re

def Tag(Data):
    Tag = pd.read_csv('data/Tag.csv')

    for index, row in Data.iterrows():

        try:
            row["Tag"] = re.sub(r".*\-", "", str(row["Tag"]))
        
            row["Tag"] = re.sub(r".{2}$", "", str(row["Tag"]))
        
            Data.set_value(index,'Tag',  row["Tag"])
            
            
            if row["Tag"] in Tag["code"].unique():
        
                x = Tag["code"].loc[Tag["code"] == row["Tag"]].index
            
                Data.loc[index, "Name"] = Tag.iloc[x[0]]["English"]
            else:
                Data.loc[index, "Name"] = "Wrong Data Input"

        except:
            pass

    return(Data)
#    print(set(Data.Name))
#    return(Data)
#    Data.to_csv("data/main.csv")


from datetime import datetime

def DateTime(Data):

#    df = pd.read_csv('data/main.csv')
    for index, row in Data.iterrows():
        try:
            row["Date/Time"] = row["Date/Time"].lstrip()
            row["Date/Time"] = row["Date/Time"][:16]
            row["Date/Time"] = datetime.datetime.strptime(row["Date/Time"], '%d/%m/%Y %H:%M')
        except:
            pass

    Data['date'] = pd.to_datetime(Data["Date/Time"])
    Data['year'], Data['month'], Data["day"], Data["hour"] = Data['date'].dt.year, Data['date'].dt.month, Data['date'].dt.day, Data['date'].dt.hour
    
    return(Data)
#    Data.to_csv("data/main.csv")


def Intensity(Data):
#    df = pd.read_csv('data/main.csv')
    Data['Intensity'] = pd.to_numeric(Data['Intensity'], errors='coerce')
    return(Data)
#    df.to_csv("data/main.csv")

def duration(Data):
#    df = pd.read_csv('data/main.csv')
    Data['Duration'] =  pd.to_datetime(Data['Duration'], format='%H:%M:%S', errors='coerce').dt.time
    Data['Duration'] = Data['Duration'].apply(lambda x: (x.hour * 60 + x.minute))
    
    return(Data)
#    df.to_csv("data/main.csv")


def Split_data(Data, current_day, current_month, current_year):

    if current_day < 5:
        current_month = current_month - 1

#    df = pd.read_csv('data/main.csv')
    Data_m = Data[(Data["year"] == current_year) & (Data["month"] == current_month)]
    Data_m.to_csv("data/main_month.csv")

    return(Data_m)

import subprocess

def create_folder(name):
    cmd = ['mkdir', 'pdf/Final/' + name]
    subprocess.call(cmd)
    print("Folder created")



