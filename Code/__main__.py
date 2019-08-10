# Set path directory
import sys, os
sys.path.append(os.path.realpath(".."))

import datetime

# Get the time now
current_time = datetime.datetime.now()

# Connect to Open Human
from fonctions import open_human

Data = open_human.token()


print("======================")
print(len(Data['results']), "users are registered")
print("======================")

# Store Data as file
from fonctions import preprocessing
from fonctions import clean
from fonctions import code
from fonctions import graph


for user in Data['results']:
    global name
    name = user['project_member_id']

    # Get the data from open human
#    n = 0
    if open_human.get_data(user) == 0:
        
    
            # save it as .csv in ../data
        Data = preprocessing.load()

        # create folder for user
        preprocessing.create_folder(name)

        # remove NA's        
        with_na = len(Data)
        Data = Data.dropna(thresh = 7)
        without_na = len(Data)
        dropped = with_na - without_na
        print(dropped, "na's were removed from data")

        # PREPROCESSING
        Data = preprocessing.Tag(Data)
        
        Data = preprocessing.DateTime(Data)
        Data = preprocessing.Intensity(Data)
        Data = preprocessing.duration(Data)

        # split Data
        Data_m = preprocessing.Split_data(Data, current_time.day, current_time.month, current_time.year)

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
        code.Json_2(Data)
        
        # Upload html
        code.upload_html_2()
        
        # Convert html in pdf
        code.convert_into_pdf(name)

        # Clean Data
        clean.clean_data()
#    except:
#        n += 1
#        clean.rm_folders()
        

# Clean PDF
clean.rm_folders()

# Build Metadata
code.metadata_build()

#print("ERROR", n)

# Sent PDF
#security = " " # security is the Token we are using to load the data
#open_human.metadata_send(access_token)