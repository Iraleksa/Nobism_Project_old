#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 22:19:39 2019

@author: valerian
"""
import os
#str1=os.getcwd()
#str2=str1.split('/')
#n=len(str2)
#path = str2[n-5] + '/' + str2[n-4] + '/' + str2[n-3] + '/' + str2[n-2] + '/'
#path = path + "Code/data/main.csv"
#%% SETTINGS
import plotnine as p9
import pandas as pd
import numpy as np
import datetime
import logging

#Data = pd.read_csv("data/main.csv")
import calendar
from datetime import date, timedelta

#%% TIME LINE 1
#Function TL_1
def TL_1 (Data):
    logging.info('======= Creating TimeLine 1=======')
    x = Data.Intensity[pd.isna(Data.Intensity) == True]
    if (len(x) == len(Data)):
       print("WARNING: All values for Intensity are NA's")
    
    else:
        Data['Minutesss'] = Data['date']
        Data['Minutesss'] = pd.to_datetime(Data['Minutesss'], errors='coerce')
        Data.date= pd.to_datetime(Data.date, errors = 'coerce')
        Data['Minutesss'] = Data['Minutesss'].dt.hour*60 + Data['Minutesss'].dt.minute
        #Data.Intensity = Data.Intensity.astype(str)
        #Data.Intensity = Data.Intensity.astype(float)
        #Data.Intensity.fillna('0', inplace=True)
        plot =(p9.ggplot(data=Data,
                             mapping=p9.aes(x='date',y='Minutesss',
                                            colour = 'Intensity'))
                        + p9.geom_point(size = 2)
                        #+ p9.geom_smooth(method="loess", se=False, color = 'tomato', size = 5)
                        + p9.theme_classic()
                        + p9.scale_colour_gradient(low = "white", high = "red", aesthetics = "colour")
                        + p9.theme(axis_text = p9.element_text(size=18),
                                   axis_title = p9.element_text(size = 18,face = 'bold'),
                                   legend_position = 'none')
                        + p9.scale_x_datetime(date_labels = '%b %y', date_breaks = '6 months')
                        + p9.labs(x='',y='Hours', colour = 'Intensity: ')
                        )
    #Creating and saving TL_1
    if (len(Data) > 0):
        #TL1 = TL_1(Data)
        plot.save(filename = 'TL_1.jpeg',
                 plot = plot,
                 path = "pdf/iteration/",
                 width = 25, height = 5,
                 dpi = 320)
    else: 
        print('Plot not created; no data found.')
    return(print('=================================TIMELINE_1 OK ============================='))
#%% TIME LINE 2
#Function TL_2
def TL_2(Data):
    print('======= Creating TimeLine 2 =======')
    x = Data.Duration[pd.isna(Data.Duration) == True]
    
    if ((len(x)+10)) >= len(Data):
       print("WARNING: All values for Duration are NA's")
    
    else:
        #Filter Symptomes and Correct Durations
        Symptomes = Data[(Data.Group == "sy") & (Data.Duration < 9999)]
        
        #Setting data with missing times
        Symptomes['Date'] = pd.to_datetime(Symptomes['Date'])
        
        if len(Symptomes) == 0:
            print('No duration for TL_2')
        else: 
            sdate = min(Symptomes["Date"])   # start date
            edate = max(Symptomes["Date"])   # end date
            delta = edate - sdate       # as timedelta
            from datetime import date, timedelta
            day = []
            for i in range(delta.days + 1):
                d= sdate + timedelta(days=i)
                day.append(d)
                
            DF = pd.DataFrame(day)
            DF.columns = ['Date']
            data_with_missing_times = pd.merge(DF, Symptomes, on='Date', how='outer')
            data_with_missing_times.Date = pd.to_datetime(data_with_missing_times.Date)
            if delta.days > 1825:
                datebreaks = '18 months'
            else:
                if delta.days > 1095:
                    datebreaks = '12 months'                
                else:
                    datebreaks = '6 months'
                
            plot = (p9.ggplot(data=data_with_missing_times,
                              mapping=p9.aes(x='Date',
                                             y='Duration'))
                + p9.geom_smooth(color = 'red', size = 5, method="loess", se=False)
                + p9.theme_classic()
                + p9.theme(axis_text = p9.element_text(size=33),
                           axis_title = p9.element_text(size = 33,face = 'bold'))
                + p9.scale_x_datetime(date_labels = '%Y-%m', date_breaks = datebreaks)
                + p9.labs(x='',y='')
                )    
            
            #Creating and saving TL_2
            if (len(data_with_missing_times) > 0):
                #TL2 = TL_2(data_with_missing_times)
                plot.save(filename = 'TL_2.jpeg',
                         plot = plot,
                         path = "pdf/iteration/",
                         width = 25, height = 5,
                         dpi = 320)
            else: 
                print('Plot not created; no data found.')
        return(print('=================================TIMELINE_2 OK ============================='))
#%% TIME LINE 3
#Function TL_3
def TL_3(Data):
    print('======= Creating TimeLine 3 =======')    
    x = Data.Intensity[pd.isna(Data.Intensity) == True]
    if (len(x) == len(Data)):
       print("WARNING: All values for Intensity are NA's")

    else:
        #Filter Symptomes
        Symptomes = Data[(Data.Group == "sy")]
        tl3 = Symptomes.groupby("Date", as_index =False, sort = False)['Intensity'].agg({'Intensity': 'mean'})
        #tl3['Day'] = range(1,(len(tl3)+1))
        #tl3 = tl3.rename(columns = {'Intensity': "Intensity_mean"})
        tl3['Date'] = pd.to_datetime(tl3['Date'])
        #Setting data with missing times
        sdate = min(tl3["Date"])   # start date
        edate = max(tl3["Date"])   # end date
        delta = edate - sdate       # as timedelta
        
        from datetime import date, timedelta
        day = []
        for i in range(delta.days + 1):
            d= sdate + timedelta(days=i)
            day.append(d)
            
        DF = pd.DataFrame(day)
        DF.columns = ['Date']
        data_with_missing_times = pd.merge(DF, tl3, on='Date', how='outer')
        if delta.days > 1825:
                datebreaks = '18 months'
        else:
            if delta.days > 1095:
                datebreaks = '12 months'
            else:
                datebreaks = '6 months'
        
        plot =(p9.ggplot(data=data_with_missing_times,
                         mapping=p9.aes(x='Date',y='Intensity'))
            + p9.geom_point(color = 'red', size = 5)
            + p9.theme_classic()
            + p9.theme(axis_text = p9.element_text(size=40),
                       axis_title = p9.element_text(size = 40,face = 'bold'))
            + p9.scale_x_datetime(date_labels = '%Y-%m', date_breaks = datebreaks)
            + p9.labs(x='',y='')
            )    
    
    #Creating and saving TL_3
    if (len(data_with_missing_times) > 5):
        #TL3 = TL_3(data_with_missing_times)
        
        plot.save(filename = 'TL_3.jpeg',
                 plot = plot,
                 path = "pdf/iteration/",
                 width = 25, height = 5,
                 dpi = 320)
    else: 
        print('Plot not created; no data found.')
    return(print('=================================TIMELINE_3 OK ============================='))
#%% TIME LINE 4
#Function TL_4
def TL_4(Data):
    print('======= Creating TimeLine 4 =======')
    #Filtering
    Data['date_4'] = Data['date'].dt.date
    tl4 = Data.groupby("date_4", sort = False, as_index = False).count()
    tl4 = tl4.iloc[:, 0:2]
    tl4 = tl4.rename(columns = {"Unnamed: 0": "n"})    
    
    sdate = min(tl4["date_4"])  # start date
    edate = max(tl4["date_4"])   # end date
    delta = edate - sdate       # as timedelta
    
#    tl4 = Data.groupby("Date", sort = False, as_index = False).count()
#    tl4 = tl4.iloc[:, 0:2]
#    tl4 = tl4.rename(columns = {"Unnamed: 0": "n"})
#    tl4['Date'] = pd.to_datetime(tl4['Date'])
    
#    #Setting data with missing times
#    sdate = min(tl4["Date"])  # start date
#    edate = max(tl4["Date"])   # end date
#    delta = edate - sdate       # as timedelta
    
    from datetime import date, timedelta    
    day = []
    for i in range(delta.days + 1):
        d= sdate + timedelta(days=i)
        day.append(d)
        
    DF = pd.DataFrame(day)
    DF.columns = ['date_4']
    data_with_missing_times = pd.merge(DF, tl4, on='date_4', how='outer')
    if delta.days > 1825:
                datebreaks = '18 months'
    else:
        if delta.days > 1095:
            datebreaks = '12 months'                
        else:
            datebreaks = '6 months'
    #Creating and saving TL_4
    
    plot =(p9.ggplot(data=data_with_missing_times,
                     mapping=p9.aes(x='date_4',y='n'))
        + p9.geom_col(fill = 'red')
        + p9.theme_classic()
        + p9.theme(axis_text = p9.element_text(size=40),
                   axis_title = p9.element_text(size = 40,face = 'bold'))
        + p9.scale_x_datetime(date_labels = '%Y-%m', date_breaks = datebreaks)
        + p9.labs(x='',y='')
        )
        
    if (len(data_with_missing_times) > 0):
        plot.save(filename = 'TL_4.jpeg',
                 plot = plot,
                 path = "pdf/iteration/",
                 width = 25, height = 5,
                 dpi = 320)
    else: 
        print('Plot not created; no data found.')
    return(print('=================================TIMELINE_4 OK ============================='))
#%% GRAPH 1
#Function Graph_1
def graph_1(Data, Data_m):
    print('======= Creating Graph_1 =======')
    x = Data.Intensity[pd.isna(Data.Intensity) == True]
    if (len(x) == len(Data)):
       print("WARNING: All values for Intensity are NA's")
    
    else:
    #Filter ever and monthly symptomes and correct Intensity
        Data_m_int = Data_m[(Data_m.Group == "sy") & (pd.isna(Data_m.Intensity) == 0)]
        Data_all_int = Data[(Data.Group == "sy") & (pd.isna(Data.Intensity) == 0)]
        
        Test_3_m = Data_m_int.groupby("Intensity", sort = True, as_index = False).count()
        Test_3_m = Test_3_m.iloc[:, 0:2]
        Test_3_m= Test_3_m.rename(columns = {"Unnamed: 0": "n"})
        
        Test_3 = Data_all_int.groupby("Intensity", sort = True, as_index = False).count()
        Test_3 = Test_3.iloc[:, 0:2]
        Test_3 = Test_3.rename(columns = {"Unnamed: 0": "n"})
        #Test_3.Intensity = Test_3.Intensity.astype(str)
    
        
        plot =(p9.ggplot(data=Test_3,
                         mapping=p9.aes(x='Intensity',y='n'))
            + p9.geom_col(fill = 'red')
            + p9.theme_classic()
            + p9.theme(axis_text = p9.element_text(size=40),
                       axis_title = p9.element_text(size = 40,face = 'bold'))
            + p9.coord_cartesian(xlim = (1,10))
            + p9.scale_x_continuous(labels = list(range(1,11)), breaks = list(range(1,11)))
            + p9.labs(x='',y='No. of attacks')
            )    
    
        plot_month =(p9.ggplot(data=Test_3_m,
                         mapping=p9.aes(x='Intensity',y='n'))
            + p9.geom_col(fill = 'red')
            + p9.theme_classic()
            + p9.theme(axis_text = p9.element_text(size=40),
                       axis_title = p9.element_text(size = 40,face = 'bold'))
            + p9.coord_cartesian(xlim = (1,10))
            + p9.scale_x_continuous(labels = list(range(1,11)), breaks = list(range(1,11)))
            + p9.labs(x='',y='No. of attacks')
            )

    #Creating and saving EVER Graph_1
    if (len(Data_m_int) > 0):
        #G1 = graph_1(Data_all_int)
        plot_month.save(filename = 'Graph_1.jpeg',
                 plot = plot_month,
                 path = "pdf/iteration/",
                 width = 25, height = 5,
                 dpi = 320)
    else: 
        print('Plot not created; no data found.')
    if (len(Data_all_int) > 0):
        #G1 = graph_1(Data_all_int)
        plot.save(filename = 'Graph_ALL_1.jpeg',
                 plot = plot,
                 path = "pdf/iteration/",
                 width = 25, height = 5,
                 dpi = 320)    
    else: 
        print('Plot not created; no data found.')
    return(print('=================================Graph_1 OK ============================='))
#%% GRAPH 2
#Function Graph_2
def graph_2(Data, Data_m):
    print('======= Creating Graph 2 =======')
    #Filter current year and month, and correct Duration
    
    #Graph2_ALL.Duration = Graph2_ALL.Duration/60
    #Graph2_ALL.Duration = Graph2_ALL.Duration.astype(str)    
    x = Data.Duration[pd.isna(Data.Duration) == True]
    if (len(x) == len(Data)):
        logging.warning('=================================Graph_2 aborted =============================')
        return
    else:
        Graph2 = Data_m[(Data_m.Duration < 10080)]
        Graph2_ALL = Data[(Data.Duration < 10080)]
        if (len(Graph2_ALL) > 0):
                    plot= (p9.ggplot(data=Graph2_ALL,
                                     mapping=p9.aes(x='Duration'))
                                + p9.geom_bar(fill = 'red', stat = 'count', size = 100)
                                + p9.theme_classic()
                                + p9.theme(axis_text = p9.element_text(size=40),
                                           axis_title = p9.element_text(size = 40,face = 'bold'))
                                + p9.labs(title = '', x='',y='No. of attacks')
                                )
                    plot.save(filename = 'Graph_ALL_2.jpeg',plot = plot,
                          path = "pdf/iteration/",
                          width = 25, height = 5,
                          dpi = 320)
        else: 
                print('Plot not created; no data found.')
        if (len(Graph2) > 0):
                    plot_month= (p9.ggplot(data=Graph2,
                                           mapping=p9.aes(x='Duration'))
                                + p9.geom_bar(fill = 'red', stat = 'count', size = 100)
                                + p9.theme_classic()
                                + p9.theme(axis_text = p9.element_text(size=40),
                                           axis_title = p9.element_text(size = 40,face = 'bold'))
                                + p9.labs(title = '', x='',y='No. of attacks')
                                )
                    plot_month.save(filename = 'Graph_2.jpeg',
                                plot = plot_month,
                                path = "pdf/iteration/",
                                width = 25, height = 5,
                                dpi = 320)
        else: 
                print('Plot not created; no data found.')
    return(print('=================================Graph_2 OK ============================='))
#%% GRAPH 3
#Function Graph_3
def graph_3(Data, Data_m):
    print('======= Creating Graph 3 =======')
    #Filter montlhy and ever Symptomes
    freq_all = Data[(Data.Group == 'sy')]
    freq_m = Data_m[(Data_m.Group == 'sy')]
    
    test = freq_all[(pd.isna(freq_all.year) == 0) & (pd.isna(freq_all.month) == 0)]
    Test_3 = pd.DataFrame(test.groupby("hour", as_index = False).count())
    Test_3 = Test_3.iloc[:, 0:2]
    Test_3 = Test_3.rename(columns = {"Unnamed: 0": "n"})

    test_m = freq_m[(pd.isna(freq_m.year) == 0) & (pd.isna(freq_m.month) == 0)]
    Test_3_m = pd.DataFrame(test_m.groupby("hour", as_index = False).count())
    Test_3_m = Test_3_m.iloc[:, 0:2]
    Test_3_m = Test_3_m.rename(columns = {"Unnamed: 0": "n"})
    
    
    plot =(p9.ggplot(data=Test_3,
                     mapping=p9.aes(x='hour', y = 'n'))
        + p9.geom_count(color ="tomato", show_legend=False)
        #+ p9.geom_point(color = 'red', size = 10)
        #+ p9.geom_line(color = 'red', size = 1)
        + p9.theme_classic()
        + p9.theme(axis_text = p9.element_text(size=40),
                   axis_title = p9.element_text(size = 40,face = 'bold'))
        + p9.coord_cartesian(xlim = (1,25))
        + p9.labs(x='Hours',y='No. of attacks')
        + p9.scale_x_discrete(limits = (range(1,25)))
        )
    plot_month =(p9.ggplot(data=Test_3_m,
                     mapping=p9.aes(x='hour', y = 'n'))
        #+ p9.geom_line(color = 'red', size = 5)
        + p9.geom_point(color = 'red', size = 10)
        + p9.geom_line(color = 'red', size = 1)
        + p9.theme_classic()
        + p9.theme(axis_text = p9.element_text(size=40),
                   axis_title = p9.element_text(size = 40,face = 'bold'))
        + p9.coord_cartesian(xlim = (1,25))
        + p9.labs(x='Hours',y='No. of attacks')
        + p9.scale_x_discrete(limits = (range(1,25)))
        )

    #Creating and saving MONTHLY Grap_3
    if (len(Test_3_m) > 0):
        #G3 = graph_3(freq_m)
        plot_month.save(filename = 'Graph_3.jpeg',
                 plot = plot_month,
                 path = "pdf/iteration/",
                 width = 25, height = 5,
                 dpi = 320)
    else: 
        print('Plot not created; no data found.')

    #Creating and saving EVER Grap_3
    if (len(freq_all) > 0):
        #G3 = graph_3(freq_all)
        plot.save(filename = 'Graph_ALL_3.jpeg',
                 plot = plot,
                 path = "pdf/iteration/",
                 width = 25, height = 5,
                 dpi = 320)
    else: 
        print('Plot not created; no data found.')

    return(print('=================================Graph_3 OK ============================='))    
#%% MEDICINE
def medicine(Data):
    print('======= Creating Medicine =======')
    #Filter medicine 
    medicine = Data[(Data.Group == 'me')|(Data.Group == 'ma')]
    med_count = len(medicine)
    #Add diff medicines to LISTE
    #diff_medicines = len(medicine['Name'].unique())
    #LISTE['diff_medicines'] = str(diff_medicines)
    
    #Setting data with missing times
    medicine.Date = pd.to_datetime(medicine.Date)
    medicine['Date'] = pd.to_datetime(medicine['Date'])
    sdate = min(medicine["Date"])   # start date
    edate = max(medicine["Date"])   # end date
    delta = edate - sdate       # as timedelta
    from datetime import date, timedelta    
    day = []
    for i in range(delta.days + 1):
        d= sdate + timedelta(days=i)
        day.append(d)
        
    DF = pd.DataFrame(day)
    DF.columns = ['Date']
    data_with_missing_times = pd.merge(DF, medicine, on='Date', how='outer')
    medicine = data_with_missing_times
    
    ########HOW TO DEAL WITH MEDICINE NA'S IN PLOTS, NOT TO SHOW THEM#############################################################################################################
    #if (medicine.Name.isnull().sum() > 0):   
        #medicine = medicine[['Date','Name']]
        #medicine = 
    
    medicine = medicine[pd.isna(medicine.Name) == False]
    #Creating and saving Medicine plot
    if (len(medicine) > 5):        
        #Plot everything but Na's
        
        f_tl1 = (p9.ggplot(data=medicine,
                         mapping=p9.aes(x='Date', y = 'Name'))
         + p9.geom_point(color = 'red', size = 3)
         + p9.theme_classic()
         + p9.theme(axis_text = p9.element_text(size= 18),
                    axis_title = p9.element_text(size = 18,face = 'bold'))
         + p9.labs(title = 'Medicine', x='Days',y='')
         )
        f_tl1.save(filename = 'Medicine.jpeg',
                    plot = f_tl1,
                    path = "pdf/iteration/",
                    width = 25, height = 5,
                    dpi = 320)
    else: 
        print('Plot not created; no data found.')

    return(print('=================================MEDICINE OK ============================='))    
#%% Extra information
#day_nb = (datetime.datetime.now() - Data.TimeLine.min()).days
#LISTE['DAY_OLD'] = str(day_nb)

# Replace NA value by 0 in the liste
#if LISTE.isnull().sum().sum() > 0:
 #       LISTE.fillna()

#####################
#list_json <- toJSON(LISTE)