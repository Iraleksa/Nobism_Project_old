# Import fonctions
from fonctions import preprocessing
from fonctions import open_human
from fonctions import graph
from fonctions import code
from fonctions import clean

import datetime
current_time = datetime.datetime.now()

# Set path directory
import sys, os
sys.path.append(os.path.realpath(".."))

# Connect to Open Human
Data = open_human.token()

print("======================")
print(len(Data['results']), "users are registered")
print("======================")
n = 0
# Loop for each users
for user in Data['results']:
    
    global name
    name = user['project_member_id']

    # Get the data from open human
    if open_human.get_data(user) == 0:
        
        try:
            # Load Data for user
            Data = preprocessing.load()
    
            # create folder for user
            preprocessing.create_folder(name)
    
            # remove NA's    
            Data = preprocessing.remove_na(Data)
    
            # PREPROCESSING
            Data = preprocessing.Tag(Data)
            Data = preprocessing.DateTime(Data)
            Data = preprocessing.Intensity(Data)
            Data = preprocessing.duration(Data)
    
            # split Data
            Data_m = preprocessing.Split_data(Data, current_time.day, 
                                              current_time.month, current_time.year)
    
            # Build Graphs
            graph.general(Data)
            graph.duration_TL(Data)
            graph.intensity_TL(Data)
            graph.frequency_TL(Data)
            graph.intensity_graph(Data,Data_m)
            graph.duration_graph(Data,Data_m)
            graph.day_night_attacks(Data,Data_m)
            graph.medicine(Data)
    
            # Replace missing imgs
            code.img_not_found()
    
            # Create Statistiques
            code.statistiques(Data)
            
            # Upload html
            code.upload_html()
            
            # Convert html in pdf
            code.convert_into_pdf(name)
    
            # Clean Data
            clean.clean_data()
            
        except Exception as ex:
            print(ex)
            n += 1
            clean.clean_data()


#Clean PDF
#clean.rm_folders()

# Build Metadata
try:
    code.metadata_build()
except:
    print("failure processing metadata")
print("ERROR", n)

# Sent PDF
#security = " " # security is the Token we are using to load the data
#open_human.metadata_send(access_token)