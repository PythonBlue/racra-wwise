import os

import split
import names
import sort
import toc
import shutil

in_string = input("Rift Apart WWise Bank Language Suffix: ")
in_skip = input("Filter only a specific soundbank(s): ")
bankPath = "banks"
if in_string == "us" or in_string == "br":
    bankPath = "banks_" + in_string
    
split.split(in_string)
    
names.names(in_string)
    
for folder in sorted(os.listdir(bankPath + os.path.sep + "wwnames" + os.path.sep)):
    if folder.endswith(".txt"):
        if in_skip != "" and in_skip not in folder.split(".txt")[0]:
            continue
        try:
            os.system('python3 wwiser.pyz -g -go "txtp' + os.path.sep + folder.split(".")[0] + '" -gw "..' + os.path.sep + '..' + os.path.sep + 'wem" -gbo -nl "' + bankPath + os.path.sep + 'wwnames' + os.path.sep + folder + '" -l "' + bankPath + os.path.sep + folder.split(".")[0] + '.bnk"')
        except:
            print("WWiser and/or wwnames.db3 not installed!")
            shutil.rmtree(bankPath)
sort.sort(in_string)

toc.toc(in_string)
shutil.rmtree(bankPath)
