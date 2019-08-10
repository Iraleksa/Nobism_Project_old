#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:03:00 2019

@author: valerian
"""
import json
import pandas as pd

def Json(Data, Data_m):
    LISTE = {}

    #Data = pd.read_csv('data/main.csv')
    #Data_m = pd.read_csv('data/main_month.csv')

    def wrong_symptome_data(Data):
        Symptomes = Data[(Data.Group == "sy")]
        wrong_duration = Symptomes[(Symptomes.Duration >= 180) | (pd.isnull(Symptomes.Intensity))]
        missing_date = Symptomes[pd.isnull(Symptomes["date"])]
        wrong_Symptomes = round(sum([len(wrong_duration), len(missing_date)]) / len(Symptomes) * 100, 1)
        return wrong_Symptomes

    if len(Data_m) > 0:
        this_month = wrong_symptome_data(Data_m)
        LISTE["Wrong_Symptomes_month"] = str(this_month)

    ever = wrong_symptome_data(Data)
    LISTE["Wrong_Symptomes_ever"] = str(ever)


    ### GENERAL METRICS

    LISTE["data_number"] = str(len(Data.index) - 1)


    x = Data_m.loc[Data_m['Duration'] < 180]
    y = x.loc[:,"Duration"].mean()
    LISTE["mean_duration_month"] = str(round(y, 1))

    x = Data.loc[Data['Duration'] < 180]
    y = x.loc[:,"Duration"].mean()
    LISTE["mean_duration_ever"] = str(round(y, 1))


    y = Data_m.loc[:,"Intensity"].mean()
    LISTE["mean_intensity_month"] = str(round(y, 1))

    y = Data.loc[:,"Intensity"].mean()
    LISTE["mean_intensity_ever"] = str(round(y, 1))


    #Cluster number
    CHs = Data[(Data["Tag"] == "14sy")]
    LISTE['Chs_number'] = str(len(CHs))

    #Watery tearing eye
    Watery_tearing_eye = Data[(Data.Tag == "89sy")]
    LISTE['Watery_tearing_eye'] = str(len(Watery_tearing_eye))

    #Neck pain
    Neck_pain = Data[(Data.Tag == "39sy")]
    LISTE['Neck_pain'] = str(len(Neck_pain))

    #Oxygen
    Oxygen = Data[(Data.Tag == "101me")]
    LISTE['Oxygen'] = str(len(Oxygen))

    #Litium
    Litium = Data[(Data.Tag == "28me")]
    LISTE['Litium'] = str(len(Litium))

    #Sumatriptan
    Sumatriptan = Data[(Data.Tag == "53me") | (Data.Tag == "54me") | (Data.Tag == "55me")]
    LISTE['Sumatriptan'] = str(len(Sumatriptan))

    #Toporimato
    Toporimato = Data[(Data.Tag == "121me")]
    LISTE['Toporimato'] = str(len(Toporimato))

    #Magic mushrooms
    Magic_mushrooms = Data[(Data.Tag == "12ma")]
    LISTE['Magic_mushrooms'] = str(len(Magic_mushrooms))

    #Vitamin D
    vit_D = Data[(Data.Tag == "11vi")]
    LISTE['vit_D'] = str(len(vit_D))

    #Magnesium
    vit_magn = Data[(Data.Tag == "5vi")]
    LISTE['vit_magn'] = str(len(vit_magn))


    # ### DAY/NIGHT


    Data_m_DC = Data.loc[Data['Duration'] < 180]

    night = Data_m_DC[((Data_m_DC.hour >= 0)&(Data_m_DC.hour <= 5))|((Data_m_DC.hour >= 21)&(Data_m_DC.hour <= 23))]
    night_duration = round(night["Duration"].mean(),1)
    night_Intensity = round(night["Intensity"].mean(),1)

    day = Data_m_DC[(Data_m_DC.hour <= 20)&(Data_m_DC.hour >= 6)]
    day_duration = round(day["Duration"].mean(),1)
    day_Intensity = round(day["Intensity"].mean(),1)


    # ### DURATION

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

    Data["date"] = pd.to_datetime(Data["date"])
    day_nb = datetime.datetime.now() - min(Data["date"])
    LISTE["DAY_OLD"] = str(day_nb.days)

    import json

    with open('pdf/iteration/data.json', 'w') as fp:
        json.dump(LISTE, fp)

    return(LISTE)



def json_file():
    print("launching Json ...")
    with open('pdf/iteration/data.json') as json_data:
        data = json.load(json_data,)
        for key, value in data.items():

# -------------- PAGE 3 ---
            if key == 'mean_duration_month':
                x = ''.join(value)
                global mean_duration_month
                mean_duration_month = x

            if key == 'mean_intensity_month':
                global mean_intensity_month
                mean_intensity_month = ''.join(value)

            if key == 'DURATION':
                global DURATION
                DURATION = ''.join(value)

            if key == 'INTENSITY':
                global INTENSITY
                INTENSITY = ''.join(value)

            if key == 'mean_intensity_ever':
                global mean_intensity_ever
                mean_intensity_ever = ''.join(value)

# ---------------- PAGE 4 ---

            if key == 'diff_medecines':
                global diff_medecines
                diff_medecines = ''.join(value)

# ---------------- PAGE 5 ---

            if key == 'Wrong_Symptomes_month':
                global Wrong_Symptomes_month
                Wrong_Symptomes_month = ''.join(value)

            if key == 'Wrong_Symptomes_ever':
                global Wrong_Symptomes_ever
                Wrong_Symptomes_ever = ''.join(value)

            if key == 'data_number':
                global data_number
                data_number = ''.join(value)

            if key == 'Chs_number':
                global Chs_number
                Chs_number = ''.join(value)

            if key == 'Watery_tearing_eye':
                global Watery_tearing_eye
                Watery_tearing_eye = ''.join(value)

            if key == 'Neck_pain':
                global Neck_pain
                Neck_pain = ''.join(value)

            if key == 'Oxygen':
                global Oxygen
                Oxygen = ''.join(value)

            if key == 'Litium':
                global Litium
                Litium = ''.join(value)

            if key == 'Sumatriptan':
                global Sumatriptan
                Sumatriptan = ''.join(value)

            if key == 'Toporimato':
                global Toporimato
                Toporimato = ''.join(value)

            if key == 'Magic_mushrooms':
                global Magic_mushrooms
                Magic_mushrooms = ''.join(value)

            if key == 'vit_D':
                global vit_D
                vit_D = ''.join(value)

            if key == 'vit_magn':
                global vit_magn
                vit_magn = ''.join(value)


            if key == 'DAY_OLD':
                global DAY_OLD
                DAY_OLD = ''.join(value)


    print("... Json : OK")


# In[7]:


DIV_LISTE = ['mean_duration_month', 'DURATION', 'INTENSITY', 'Neck_pain', 'vit_D', 'Oxygen', 'DAY_OLD', 'vit_magn',
             'Litium', 'Magig_nushrooms', 'Watery_tearing_eye', 'Toporimato', 'Chs_number', 'data_number',
             'Wrong_data_ever', 'Wrong_data_month', 'mean_Intensity_month', 'mean_Intensity_ever', 'diff_medicines']

import time
import bs4

def upload_html():
    print("launching HTML ...")

    # Import HTML
    f = open('pdf/template/index.html', 'r')
    html = f.read()
    soup = bs4.BeautifulSoup(html, features="html5lib")

# ------ PAGE 3 ---
    Div_1 = soup.find("div", {"id": "mean_duration_month"})
    Div_1.clear()
    Div_1.insert(1, mean_duration_month)

    Div_1 = soup.find("div", {"id": "mean_Intensity_month"})
    Div_1.clear()
    Div_1.insert(1, mean_intensity_month)

    Div_1 = soup.find("div", {"id": "DURATION"})
    Div_1.clear()
    Div_1.insert(1, DURATION)

    Div_1 = soup.find("div", {"id": "INTENSITY"})
    Div_1.clear()
    Div_1.insert(1, INTENSITY)

    Div_1 = soup.find("div", {"id": "mean_Intensity_ever"})
    Div_1.clear()
    Div_1.insert(1, mean_intensity_ever)

# ------ PAGE 4 ---

    Div_1 = soup.find("div", {"id": "diff_medicines"})
    Div_1.clear()
    Div_1.insert(1, diff_medecines)

# ------- PAGE 5 ---

    Div_1 = soup.find("div", {"id": "Wrong_data_month"})
    Div_1.clear()
    Div_1.insert(1, Wrong_Symptomes_month)

    Div_1 = soup.find("div", {"id": "Wrong_data_ever"})
    Div_1.clear()
    Div_1.insert(1, Wrong_Symptomes_ever)

    Div_1 = soup.find("div", {"id": "data_number"})
    Div_1.clear()
    Div_1.insert(1, data_number)

    Div_1 = soup.find("div", {"id": "Chs_number"})
    Div_1.clear()
    Div_1.insert(1, Chs_number)

    Div_1 = soup.find("div", {"id": "Watery_tearing_eye"})
    Div_1.clear()
    Div_1.insert(1, Watery_tearing_eye)

    Div_1 = soup.find("div", {"id": "Neck_pain"})
    Div_1.clear()
    Div_1.insert(1, Neck_pain)

    Div_1 = soup.find("div", {"id": "Oxygen"})
    Div_1.clear()
    Div_1.insert(1, Oxygen)

    Div_1 = soup.find("div", {"id": "Litium"})
    Div_1.clear()
    Div_1.insert(1, Litium)

    Div_1 = soup.find("div", {"id": "Sumatriptan"})
    Div_1.clear()
    Div_1.insert(1, Sumatriptan)

    Div_1 = soup.find("div", {"id": "Toporimato"})
    Div_1.clear()
    Div_1.insert(1, Toporimato)

    Div_1 = soup.find("div", {"id": "Magig_nushrooms"})
    Div_1.clear()
    Div_1.insert(1, Magic_mushrooms)

    Div_1 = soup.find("div", {"id": "vit_D"})
    Div_1.clear()
    Div_1.insert(1, vit_D)

    Div_1 = soup.find("div", {"id": "vit_magn"})
    Div_1.clear()
    Div_1.insert(1, vit_magn)

    Div_1 = soup.find("div", {"id": "DAY_OLD"})
    Div_1.clear()
    Div_1.insert(1, DAY_OLD)


    with open("pdf/template/index.html", "w") as outf:
        outf.write(str(soup))

    time.sleep(30)

    print("... HTML : OK")


from datetime import datetime
import pdfkit

#from io import BytesIO
#from django.http import HttpResponse
#from django.template.loader import get_template
#import xhtml2pdf.pisa as pisa
#from django.conf import settings
#settings.configure()
#
#sourceHtml = "index.html"
#
#        template = get_template('index.html')
#        html = template.render(params)
#        response = BytesIO()
#        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
#        if not pdf.err:
#            return HttpResponse(response.getvalue(), content_type='application/pdf')
#        else:
#            return HttpResponse("Error Rendering PDF", status=400)
#

# Define your data



# Utility function
def convertHtmlToPdf(name):
    from datetime import datetime
    y = datetime.now()
    m = y.month
    y = y.year
    path = 'pdf/Final/' + name + '/' + str(y) + '-' + str(m) + '_' + 'Nobism.pdf'
    sourceHtml = "pdf/template/index.html"
    template = open(sourceHtml)
    # open output file for writing (truncated binary)
    resultFile = open(path, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(template.read(), resultFile, "w")

    # close output file
    resultFile.close()
    template.close()
    # return True on success and False on errors
    return pisaStatus.err

from xhtml2pdf import pisa
from io import StringIO
from django.template.loader import get_template
from django.template import Context

def html_to_pdf_directly(request):
	template = get_template("pdf/template/index.html")
	context = Context({'pagesize':'A4'})
	html = template.render(context)
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html), dest=result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	else: return HttpResponse('Errors')

def convert_into_pdf(name):
    from datetime import datetime
    current_time = datetime.now()
    m = current_time.month
    y = current_time.year
    options = {'orientation': 'Landscape'}
#    config = pdfkit.configuration(wkhtmltopdf=r"/usr/local/bin/wkhtmltopdf")
    path = 'pdf/Final/' + name + '/' + str(y) + '-' + str(m) + '_' + 'Nobism.pdf'
    pdfkit.from_file("pdf/template/index.html", path, options = options)

import pandas as pd

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
    current_path =  os.getcwd()
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
            print('Graph', p, 'was missing')
            cmd = ['cp', current_path + '/pdf/iteration/Logos/nodata.jpeg',
                   current_path + '/pdf/iteration/' + p]
            subprocess.call(cmd, universal_newlines=True)





