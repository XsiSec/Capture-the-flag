#usr/bin/env python
import os
import requests
import zipfile
import textract
import re
import string
matchList=[] #create a empty matchlist
url = 'https://storage.googleapis.com/gctf-2018-attachments/5a0fad5699f75dee39434cc26587411b948e0574a545ef4157e5bf4700e9d62a' #url to fetch for the request

current_working_directory = os.getcwd() #existing directory.
raw_filename = url.split('/')[-1] # get the filename.
filename=raw_filename+'.zip' # created a filename with extension.
locationForDownload = os.path.join(current_working_directory+'/Downloaded/') # created string for download location.
def downloadCTF_Material(url):
    for x in os.listdir(current_working_directory): #if there is files in current directory..
        data = len(x)
        currentFile = (x)
    if data==64: #check if the filename have 64 char long since that's the file regardless if it changes on server-side.
        print('file already exists:\n'+currentFile+'\n')
    else:
        #print('no file here')
        r = requests.get(url) # if no files exists use 'GET' method for the request
        if os.path.isdir(locationForDownload)== True: #if the 'Downloaded', folder exists alert.
            print('--------Following directory already exists:--------\n'+ locationForDownload)
            print('---------------------------------------------------')
        else:
            os.mkdir(locationForDownload) #if not create the directory.
            print('Creates following directory:\n'+locationForDownload)

        f = open(locationForDownload+raw_filename,'wb') #initalize the file 'f'
        f.write(r.content) # write to the initalized 'f'
        os.rename(locationForDownload+raw_filename,locationForDownload+filename) # rename the file since it's RAW we make a ".zip".

def unzip_file(fullname):
    zip_ref = zipfile.ZipFile(locationForDownload+filename, 'r')
    zip_ref.extractall(locationForDownload) #extract the file
    zip_ref.close() #close the Zip method.
    os.remove(locationForDownload+filename) #remove old zip file.

def viewFileInfo(path,file):
    pattern = r"(CTF)(ctf)|(^c|C)(t|T)(f|F)({).+(})|(ctf)|(CTF)" #'regex to find the flag inside the "*.pdf"'
    print('\n\n------------file-information:------------')
    #print("location:\n {} \n filename:\n {}".format(path,file))
    for y in os.listdir(path):
        if(y).endswith('.pdf'): #if file ends with extension ".pdf"
            pdf_file= os.path.join(path+y) #create the full path + existing found file.
            open_pdf_file = open(pdf_file, 'rb')
            pdf_string = textract.process(pdf_file) #extract the words from the pdf
            number_of_words = len (re.findall(r'\w+',pdf_string)) #count words from extracted pdf.
            print('\n\n---------Extract Words from PDF:---------\n--------------------{}-------------------'.format(number_of_words))

            for z in pdf_string.split():#seperate the whole text string into own words.
                filtered_string = filter(lambda x: x in string.printable, z) #escape all ascii chars such as invisble etc.
                matches = re.finditer(pattern, z, re.MULTILINE)
                for matchNum, match in enumerate(matches):#enumerate the matches
                    matchNum = matchNum + 1
                    print ("{matchNum} match found at line and character:{start}-{end}:\nFOUND:\n{match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
                    matchString=str("{match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
                    matchList.append(matchString)
                    print('-----------------------------------------')
        else:
            #print('no pdfs found')
            continue

def writeFlagToFile():
    print('---Writes matchList to a new textfile----')
    file = open(locationForDownload+'captured_flag1.txt', 'w') # write to textfile.
    for y in matchList: #write all matches from the 'matchList' into a new text-file.
        file.write(y)
        file.close()

downloadCTF_Material(url)
unzip_file(filename)
viewFileInfo(locationForDownload,filename)
writeFlagToFile()
