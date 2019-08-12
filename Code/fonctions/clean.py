import subprocess

def clean_data():
    # Clean images
    subprocess.call('rm pdf/iteration/*.jpeg', shell=True)
    print("Images removed")

    # Clean Data
    subprocess.call('rm data/main.csv', shell=True)
    print("Images removed")


def rm_folders():
    subprocess.call('rm -r pdf/Final/*', shell = True)
    print("PDF removed")
