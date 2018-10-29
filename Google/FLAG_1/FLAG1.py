#usr/bin/env python
import os
import requests
import zipfile
import textract
import re
import string

url = ('https://storage.googleapis.com/gctf-2018-attachments/5a0fad5699f75dee39434cc26587411b948e0574a545ef4157e5bf4700e9d62a')

current_working_directory = os.getcwd()
raw_filename = url.split('/')[-1]
filename=raw_filename+'.zip'
locationForDownload = os.path.join(current_working_directory+'/Downloaded/')

def downloadCTF_Material(url):
    for x in os.listdir(current_working_directory):
        data = len(x)
        currentFile = (x)
    if data==64:
        print('file already exists:\n'+currentFile+'\n')
    else:
        #print('no file')
        r = requests.get(url)
        if os.path.isdir(locationForDownload)== True:
            print('--------Following directory already exists:--------\n'+ locationForDownload)
            print('---------------------------------------------------')
        else:
            os.mkdir(locationForDownload)
            print('Creates following directory:\n'+locationForDownload)

        f = open(locationForDownload+raw_filename,'wb')
        f.write(r.content) # I GUESS ITS here I set location?
        os.rename(locationForDownload+raw_filename,locationForDownload+filename)

def unzip_file(fullname):
    zip_ref = zipfile.ZipFile(locationForDownload+filename, 'r')
    zip_ref.extractall(locationForDownload)
    zip_ref.close()
    os.remove(locationForDownload+filename)

def viewFileInfo(path,file):
    pattern = r"(CTF)(ctf)|(^c|C)(t|T)(f|F)({).+(})|(ctf)|(CTF)"
    print('\n\n------------file-information:------------')
    #print("location:\n {} \n filename:\n {}".format(path,file))
    for y in os.listdir(path):
        if(y).endswith('.pdf'):
            pdf_file= os.path.join(path+y)
            open_pdf_file = open(pdf_file, 'rb')
            pdf_string = textract.process(pdf_file)
            number_of_words = len (re.findall(r'\w+',pdf_string))
            print('\n\n---------Extract Words from PDF:---------\n--------------------{}-------------------'.format(number_of_words))

            for z in pdf_string.split():
                filtered_string = filter(lambda x: x in string.printable, z) #escape all ascii chars such as invisble etc.
                matches = re.finditer(pattern, z, re.MULTILINE)
                for matchNum, match in enumerate(matches):
                    matchNum = matchNum + 1
                    print ("{matchNum} match found at line and character:{start}-{end}:\nFOUND:\n{match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

        else:
            print('no pdfs found')

downloadCTF_Material(url)
unzip_file(filename)
viewFileInfo(locationForDownload,filename)
