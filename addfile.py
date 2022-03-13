# Programma che sposta un singolo file (che si trova nella cartella files) nella sottocartella di competenza, aggiornando il recap.
# L'interfaccia dell'eseguibile ha come unico argomento (obbligatorio) il nome del file da spostare (comprensivo di formato, es: 'trump.jpeg'). 
# Nel caso in cui il file passato come argomento non esista, l'interfaccia deve comunicarlo all'utente.

import sys
import argparse
import os
from shutil import move, Error 
import csv
import itertools


# Verifies if the directory of reference for file search is \files
cur_dir = os.getcwd()
if not cur_dir.endswith('files'):
    cur_dir = os.path.join(cur_dir, 'files')

extentions = {'images':['.png', '.jpg', '.jpeg'], 'docs':['.txt', '.odt'], 'audio':['.mp3']}

extentions_list = list(itertools.chain(extentions['images'],extentions['docs'], extentions['audio']))

# Extracts the sorted list of files present in directory \files
src_names = sorted(os.listdir(cur_dir)) 

# Evaluates extracted files against allowed extensions
files_to_move = [ str(value) for value in src_names if os.path.splitext(value)[1] in extentions_list]

if (files_to_move == []):
    sys.exit( "There aren't any new files to be moved")

# Using the standard argparse library for CLI insertion
parser = argparse.ArgumentParser(description='Add a file to its corresponding subfolder')
parser.add_argument("filename", type=str, choices = files_to_move,
                    help="move the specified file, es: 'trump.jpeg', to its correspondant subdirectory")  # required argument
parser.add_argument("-v", "--verbose", action="store_true",
                    help="The file to be moved it is stored at path ../files")              # optional argument
args = parser.parse_args()                                                                  # args holds all specified arguments on the terminal

# Composes the complete path of the file to be moved
file_to_move = os.path.join(cur_dir, args.filename)

file_info = {'name': '', 'type': '', 'size': 0 }   # will contain file's info such as name, type and size

errors = []                                        # will collect the catched errors 

# Creates the csv file if it doesn't exists and writes down the csv columns header
csv_file = os.path.join(cur_dir, 'recap.csv')
if not os.path.isfile(csv_file):
    with open('files/recap.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['name'] + ['type'] + ['size(B)'])
    

try:
    file_info['name'] = os.path.splitext(sys.argv[1])[0]               # extracts from the tuple only the file name (no ext) and insert it into the dict.
    
    folder = [ key for key, value in extentions.items() if os.path.splitext(sys.argv[1])[1] in value]               # a list that contains the name of the destination folder 
    
    dst_dir_name = folder[0]                       # extracts the string from the list
 
    if dst_dir_name != 'audio':
        file_info['type'] = dst_dir_name[:-1]      # removes the last "s" from words "images" and "docs"
    else:
        file_info['type'] = dst_dir_name           # if dst_dir_name is "audio" it doesn't require trimming
        
    dst_dir = os.path.join(cur_dir, dst_dir_name)  # composes the destination path (stopping at dir level)
    if not os.path.isdir(dst_dir):                 # if the directory doesn't exist, os module creates it
        os.makedirs(dst_dir)
    
    dst_file = os.path.join(dst_dir, sys.argv[1])         # composes the complete destination path containing also the name of the file
    file_info['size'] = os.path.getsize(file_to_move)  # gets the size in bytes of the src_file
    
    if not os.path.isfile(dst_file):               # if the file doesn't already exist in the directory, os module moves it
        move(file_to_move, dst_dir)
    else:
        sys.exit("There is already a file with this name in the destination folder")
        
    # prints file's info: name, type and size 
    print("%s type:%s size:%dB" % (file_info['name'], file_info['type'], file_info['size']))   
        
    # writes file's info into the recap.csv file
    with open('files/recap.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([file_info['name'],file_info['type'],str(file_info['size'])])
        
    
# catch the errors so that we can continue with other files
except Error as err:
    errors.append("Shutil Error: " + err.args[0])            

except OSError as err:
    errors.append("OSError: " + err.args[0])   

if errors:
    raise Error(errors)