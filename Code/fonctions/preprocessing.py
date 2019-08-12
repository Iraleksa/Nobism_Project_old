#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:00:44 2019

@author: valerian
"""


import pandas as pd
import re
from datetime import datetime
import subprocess


def load():
    Data = pd.read_csv('data/main.csv')
    return(Data)
    

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


def DateTime(Data):
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



def Intensity(Data):
    Data['Intensity'] = pd.to_numeric(Data['Intensity'], errors='coerce')
    return(Data)

def duration(Data):
    Data['Duration'] =  pd.to_datetime(Data['Duration'], format='%H:%M:%S', errors='coerce').dt.time
    Data['Duration'] = Data['Duration'].apply(lambda x: (x.hour * 60 + x.minute))
    
    return(Data)

def Split_data(Data, current_day, current_month, current_year):

    if current_day < 5:
        current_month = current_month - 1

    Data_m = Data[(Data["year"] == current_year) & (Data["month"] == current_month)]
    Data_m.to_csv("data/main_month.csv")

    return(Data_m)


def create_folder(name):
    cmd = ['mkdir', 'pdf/Final/' + name]
    subprocess.call(cmd)
    print("Folder created")
    
def remove_na(Data):
    with_na = len(Data)
    clean_Data = Data.dropna(thresh = 7)
    without_na = len(clean_Data)
    dropped = with_na - without_na
    print(dropped, "na's were removed from data")
    return(clean_Data)



