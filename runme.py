import os

import split
import names
import sort
import toc
import shutil

in_string = input("Rift Apart WWise Bank Language Suffix: ")
in_skip = input("Filter only a specific soundbank(s): ")
bankPath = "banks"
validType = in_string == "us"
if validType == False:
    validType = in_string == "fr"
if validType == False:
    validType = in_string == "de" or in_string == "it" or in_string == "jp"
if validType == False:
    validType = in_string == "pl" or in_string == "ru"
if validType == False:
    validType = in_string == "es" or in_string == "br"
if validType == False:
    validType = in_string == "la"
if validType == True:
    bankPath = "banks_" + in_string
    
split.split(in_string, validType)
    
names.names(in_string, validType)

debug = False
    
for folder in sorted(os.listdir(bankPath + os.path.sep + "wwnames" + os.path.sep)):
    if folder.endswith(".txt"):
        if in_skip != "" and in_skip not in folder.split(".txt")[0]:
            continue
        if folder.split(".txt")[0] == "init":
            continue
        if os.path.exists("wwiser.pyz") and os.path.exists("wwnames.db3"):
            os.system('python3 wwiser.pyz -nl "' + bankPath + os.path.sep + 'wwnames' + os.path.sep + folder + '" -l "' + bankPath + os.path.sep + folder.split(".")[0] + '.bnk" "' + bankPath + os.path.sep + 'init.bnk"')
            os.system('python3 wwiser.pyz -g -gu -gr "([A-Z_]*)=:" -go "' + bankPath + os.path.sep + 'txtp' + os.path.sep + folder.split(".")[0] + '" -gd -gw "..' + os.path.sep + '..' + os.path.sep + 'wem" -gbo -nl "' + bankPath + os.path.sep + 'wwnames' + os.path.sep + folder + '" -l "' + bankPath + os.path.sep + folder.split(".")[0] + '.bnk" "' + bankPath + os.path.sep + 'init.bnk"')
        else:
            print("WWiser and/or wwnames.db3 not installed!")
            debug = True

if debug == False:
    sort.sort(in_string, validType)
    toc.toc(in_string, validType)
shutil.rmtree(bankPath)
