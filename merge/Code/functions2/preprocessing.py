#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:00:44 2019

@author: valerian
"""


import pandas as pd

def load():
    dateCols = ['Date/Time']
    #dtypes = {'Date/Time':'pd.to_datetime()'}
    Data = pd.read_csv('data/main.csv', parse_dates = dateCols)
    return(Data)

import re

def Tag(Data):
    Tag = pd.read_csv('data/Tag.csv')
    #Data = pd.read_csv('data/main.csv')


    for index, row in Data.iterrows():
        try:
            row["Tag"] = re.sub(r"^.+-", "", str(row["Tag"]))
            x = re.sub(r".{2}$", "", str(row["Tag"]))
            Data.set_value(index,'Tag', x)
            x = Tag["code"].loc[Tag["code"] == row["Tag"]].index
            Data.loc[index, "Name"] = Tag.iloc[x[0]]["English"]

        except:
            pass

    return(Data)


def DateTime(Data):
    import numpy as np
    from datetime import datetime
    Data['date'] = Data['Date/Time']
    del Data['Date/Time']
    Data['year'], Data['month'], Data["day"], Data["hour"] = Data['date'].dt.year, Data['date'].dt.month, Data['date'].dt.day, Data['date'].dt.hour
    del Data['Date'] 
    Data['Date'] = Data.date.dt.date
    Data['Date'] = Data['Date'].apply((lambda x: datetime.strftime(x,'%d/%m/%Y')))
    Data['date'] = Data['date'].apply((lambda x: datetime.strftime(x,'%d/%m/%Y %H:%M:%S')))
    return(Data)


def Intensity(Data):
    #df = pd.read_csv('data/main.csv')
    Data['Intensity'] = pd.to_numeric(Data['Intensity'], errors='coerce')
    #df.to_csv("data/main.csv")
    return(Data)

def duration(Data):
    #df = pd.read_csv('data/main.csv')
    Data['Duration'] =  pd.to_datetime(Data['Duration'], format='%H:%M:%S', errors = 'coerce').dt.time
    Data['Duration'] = Data['Duration'].apply(lambda x: (x.hour * 60 + x.minute))
    #df.to_csv("data/main.csv")
    return(Data)

def Split_data(Data, current_day, current_month, current_year):

    if current_day < 5:
        current_month = current_month - 1

    #df = pd.read_csv('data/main.csv')
    Data_m = Data[(Data["year"] == current_year) & (Data["month"] == current_month)]
    #Data_m.to_csv("data/main_month.csv")
    return(Data_m)
import subprocess

def create_folder(name):
    import os
    current_path = os.getcwd()
    cmd = ['mkdir', current_path + '/pdf/Final/' + name]
    subprocess.call(cmd)
    print("Folder created")



