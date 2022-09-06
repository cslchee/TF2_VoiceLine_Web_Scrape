import requests, os
from bs4 import BeautifulSoup
from time import sleep
from tkinter import filedialog
import urllib.request

def main():
    print("Note: Currently using as delay")
    # Make Directories
    mainDir = filedialog.askdirectory()
    classes = ('Soldier', 'Scout', 'Pyro',
               'Demoman', 'Heavy', 'Engineer',
               'Medic', 'Sniper', 'Spy')
    folder_name = 'TF2 Voice Lines Categorized'
    new_dir = f'{mainDir}/{folder_name}'
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    wiki_url = 'https://wiki.teamfortress.com/wiki/'

    for class_type in classes:
        print(f'Getting lines for {class_type}!')
        new_dir = f'{mainDir}/{folder_name}/{class_type}'
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)
        for vl_type in ('responses', 'voice commands'):
            new_dir = f'{mainDir}/{folder_name}/{class_type}/{vl_type.title()}'
            if not os.path.isdir(new_dir):
                os.mkdir(new_dir)

            url = f'{wiki_url}{class_type}_{vl_type.replace(" ","_")}'
            soup = BeautifulSoup(requests.get(url).text, "html.parser")

            #Name and grab the file at any link of the page the leads to a '.wav' file
            all_links = soup.findAll('a')
            for link in all_links:
                if link.has_attr('href'):
                    hrefStr = link['href']
                    if hrefStr.endswith('.wav'):
                        #Process text
                        text_edit = link.text
                        for remove_char in ('"','?',',','[',']','*','(apostrophe) ','/','\\','|',':','>','<'):
                            text_edit = text_edit.replace(remove_char,'')
                        if 'Translation' in text_edit: #medic lines
                            text_edit = text_edit[:text_edit.index(' (Translation')]
                        text_edit = text_edit.replace('  ', ' ')

                        file_name = hrefStr.split('/')[-1].replace('.wav','') + '__' + text_edit + '.wav'
                        file_name = file_name.replace('..wav','.wav') #redundant period next to '.wav'

                        #Prepare and download
                        wavDir = f'{new_dir}/{file_name}'
                        wavURL = f'https://wiki.teamfortress.com{hrefStr}'
                        if not os.path.isfile(wavDir):
                            print(f'\tGetting: {file_name}')
                            try:
                                urllib.request.urlretrieve(wavURL, wavDir)
                            except Exception as e:
                                print("\t\tERROR:", e)

                            sleep(0.5) #Don't overwhelm the website
                        else:
                            print(f'\tAlready have: {file_name}')


if __name__ == '__main__':
    main()

