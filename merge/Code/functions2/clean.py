import subprocess

def clean_data():
    import os
    current_path = os.getcwd()
    # Clean images
    subprocess.call('rm ' + current_path + '/pdf/iteration/*', shell=True)
    print("Images removed")

    # Clean text
    subprocess.call('rm ' + current_path + '/pdf/iteration/data.json', shell=True)
    print("Text removed")

    # Clean Data
    subprocess.call('rm ' + current_path + '/data/main.csv', shell=True)
    print("Images removed")


def rm_folders():
    import os
    current_path = os.getcwd()
    subprocess.call('rm -r ' + current_path +  '/pdf/Users/*', shell = True)
    print("PDF removed")


def nas_removal(Data):
    Data = Data.dropna(thresh = 6)
    return(Data)
