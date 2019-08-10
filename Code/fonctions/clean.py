import subprocess

def clean_data():
    # Clean images
    subprocess.call('rm pdf/iteration/*', shell=True)
    print("Images removed")

    # Clean text
    subprocess.call('rm pdf/iteration/text.json', shell=True)
    print("Text removed")

    # Clean Data
    subprocess.call('rm data/main.csv', shell=True)
    print("Images removed")


def rm_folders():
    subprocess.call('rm -r pdf/Users/*', shell = True)
    print("PDF removed")
