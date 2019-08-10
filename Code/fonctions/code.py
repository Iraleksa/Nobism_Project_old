#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:03:00 2019

@author: valerian
"""
#import numpy as np
import pdfkit

def convert_into_pdf(name):
    from datetime import datetime
    y = datetime.now()
    m = y.month
    y = y.year
    options = {'orientation': 'Landscape'}
    path = 'pdf/Final/' + name + '/' + str(y) + '-' + str(m) + '_' + 'Nobism.pdf'
    pdfkit.from_file("pdf/template/index.html", path, options = options)

import pandas as pd

import time

def metadata_build():

    # Create Metadata
    cmd = ['ohproj-upload-metadata', '-d', 'pdf/Final', '--create-csv', 'metadata.csv']
    subprocess.call(cmd, universal_newlines=True)
    time.sleep(60)
    print('OK 1')

    # Import it
    metadata = pd.read_csv("metadata.csv")
    print('OK 2')

    # Edit it
    metadata['tags'] = "Nobism"
    metadata['description'] = "Personal Monthly Report"

    #Save it
    metadata.to_csv('metadata.csv', sep=',', index=False)

    print('Metadata OK')

import os

import subprocess

def img_not_found():

    files = []

    # r=root, d=directories, f = files
    for r, d, f in os.walk("pdf/iteration/"):
        for file in f:
            if '.jpeg' in file:
                files.append(file)

    Plots = ['Graph_ALL_1.jpeg', 'Graph_1.jpeg', 'Graph_2.jpeg', 'Graph_3.jpeg', 'TL_4.jpeg',
             'TL_2.jpeg', 'TL_1.jpeg', 'Graph_ALL_3.jpeg', 'TL_3.jpeg', 'Graph_ALL_2.jpeg', 'Medicine.jpeg']

    for p in Plots:
        if p not in files:
#            print('Graph', p, 'was missing')
            cmd = ['cp', 'pdf/iteration/Logos/nodata.jpeg', 'pdf/iteration/' + p]
#            print(os.getcwd())
            subprocess.call(cmd, universal_newlines=True)



def List_Tag(Tag):
#    import os
#    print(os.getcwd())

    for (columnName, columnData) in Tag.iteritems():
        if columnName == "code":
            global x
            x = columnData.values

    return(x)

def List_Data(Data, TAG):

    LISTE = {}

    for x in TAG:
        Y = Data[(Data["Tag"] == x)]
        LISTE[x] = str(len(Y))
    return(LISTE)

def Top_Five(Data):
    filt = ["sy", "me", "ma", "vi"]
    ALL = {}
    for x in filt:
        newDict = {}
        for key, value in Data.items():
            if str(key).endswith(x):
                newDict[key] = value
        sorted_x = sorted(newDict.items(), key=lambda x: int(x[1]), reverse=True)
        y = sorted_x[:3]
        ALL[x] = y

    return(ALL)

def replace_name(Data, Tag, Lang = 2):
    FINAL = {}
    for k, v in Data.items():
        Final = []
        for y in v:
            x = Tag["code"].loc[Tag["code"] == y[0]].index
            r = Tag.iloc[x[0], Lang]
            y = list(y)
            y[0] = r
            Final.append(y)
        FINAL[k] = Final
    return FINAL

def wrong_symptome_data(Data):
    Symptomes = Data[(Data.Group == "sy")]
    wrong_duration = Symptomes[(Symptomes.Duration >= 180) | (pd.isnull(Symptomes.Intensity))]
    missing_date = Symptomes[pd.isnull(Symptomes["Date/Time"])]
    try:
        wrong_Symptomes = round(sum([len(wrong_duration), len(missing_date)]) / len(Symptomes) * 100, 1)
        return wrong_Symptomes
    except:
        wrong_Symptomes = 0
        return wrong_Symptomes

def all_buttons(Data):

    import datetime

    LISTE = {}

    LISTE["data_size"] = str(len(Data.index) - 1)

    Data["date"] = pd.to_datetime(Data["date"])
    day_nb = datetime.datetime.now() - min(Data["date"])

    LISTE["Period"] = str(day_nb.days)

    Data_m = pd.read_csv('data/main_month.csv')

    this_month = wrong_symptome_data(Data_m)
    LISTE["Wrong_Symptomes_month"] = str(this_month)

    ever = wrong_symptome_data(Data)
    LISTE["Wrong_Symptomes_ever"] = str(ever)

    x = Data_m.loc[Data_m['Duration'] < 180]
    if not isinstance(x, int):
        y = 0    
    else:
        y = x.loc[:,"Duration"].mean()
    LISTE["mean_duration_month"] = str(round(y, 1))

    x = Data.loc[Data['Duration'] < 180]
    y = x.loc[:,"Duration"].mean()
    LISTE["mean_duration_ever"] = str(round(y, 1))


    y = Data_m.loc[:,"Intensity"].mean()
    if not isinstance(y, int):
        y = 0
    LISTE["mean_intensity_month"] = str(round(y, 1))

    LISTE["mean_intensity_month_2"] = LISTE["mean_intensity_month"]

    y = Data.loc[:,"Intensity"].mean()
    LISTE["mean_intensity_ever"] = str(round(y, 1))

    Data_m_DC = Data.loc[Data['Duration'] < 180]

    night = Data_m_DC[((Data_m_DC.hour >= 0)&(Data_m_DC.hour <= 5))|((Data_m_DC.hour >= 21)&(Data_m_DC.hour <= 23))]
    night_duration = round(night["Duration"].mean(),1)
    night_Intensity = round(night["Intensity"].mean(),1)

    day = Data_m_DC[(Data_m_DC.hour <= 20)&(Data_m_DC.hour >= 6)]
    day_duration = round(day["Duration"].mean(),1)
    day_Intensity = round(day["Intensity"].mean(),1)

    ### DURATION

    DURATION = []
    if (day_duration > night_duration):
        DURATION = "The crisis were longer during the day ({} minutes) than during night ({} minutes).".format(day_duration, night_duration)
    elif (day_duration < night_duration):
        DURATION = "The crisis were longer during night ({} minutes) than during day ({} minutes).".format(night_duration, day_duration)
    elif (day_duration == night_duration):
        DURATION = "The crises has the same duration between day and night ({} minutes).".format(day_duration)

    LISTE["DURATION"] = DURATION


    # ### INTENSITY

    INTENSITY = []
    if (day_Intensity > night_Intensity):
        INTENSITY = "They were generally stronger during the day ({} against {} for the night).".format(day_Intensity, night_Intensity)
    elif (day_Intensity < night_Intensity):
        INTENSITY = "They were generaly stronger during night ({} against {} for the day).".format(night_Intensity, day_Intensity)
    elif (day_Intensity == night_Intensity):
        INTENSITY = "The global intensity is of {} with no differences between night and day.".format(day_Intensity)

    LISTE["INTENSITY"] = INTENSITY

    Med = Data[(Data.Group == "me") | (Data.Group == "ma")]
    LISTE["diff_medecines"] = str(len(set(Med.Name)))


    import datetime

    filt = ["sy", "me", "ma", "vi", "th", "fo"]

    for x in filt:
        Y = Data[(Data["Group"] == x)]
        LISTE[x] = str(len(Y))
#    LISTE["all"] = str(len(Data["Group"]) - 1)

    return LISTE


def Json_2(Data):
    Tag = pd.read_csv('data/Tag.csv')
#    Data = pd.read_csv('data/main.csv')

    all_tag = List_Tag(Tag)

    number_by_tags = List_Data(Data, all_tag)
    top_three = Top_Five(number_by_tags)

    number_by_cat = all_buttons(Data)

    global LISTE
    LISTE = replace_name(top_three, Tag)

    LISTE["cat"] = number_by_cat

import bs4

def upload_html_2():

    f = open('pdf/template/index.html', 'r')
    html = f.read()
    soup = bs4.BeautifulSoup(html, features="html5lib")

    for F in ["sy", "me", "ma", "vi"]:

        for n in range(3):

            x = str(F) + "[0][" + str(n) + "]"

            Div_1 = soup.find("div", {"id": F + "_0_" + str(n)})
            Div_1.clear()
            Div_1.insert(1, LISTE[F][n][0])

            x = str(F) + "[1][" + str(n) + "]"

            Div_1 = soup.find("div", {"id": F + "_1_" + str(n)})
            Div_1.clear()
            Div_1.insert(1, LISTE[F][n][1])

    for x in ["sy", "me", "ma", "vi", "th", "fo", "all", "Period",
              "data_size", "mean_intensity_ever", "mean_intensity_month",
              "mean_duration_month", "mean_intensity_month_2",
              "Wrong_Symptomes_month", "diff_medecines", "INTENSITY",
              "DURATION", "Wrong_Symptomes_ever"]:
        # "mean_duration_ever",

        try:
            Div_1 = soup.find("div", {"id": x})
            Div_1.clear()
            Div_1.insert(1, LISTE["cat"].get(x))

        except:
            pass


    with open("pdf/template/index.html", "w") as outf:
        outf.write(str(soup))

    print("... HTML : OK")