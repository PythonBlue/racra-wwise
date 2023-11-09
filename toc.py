import os
import shutil
import subprocess
import re
import shutil

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def toc(in_string, validType):
    bankPath = "banks"
    soundPath = "sound"
    flacPath = "flac"
    in_file_sb = open("tmp", "wb")
    if validType == True:
        in_file_sb.close()
        in_file_sb = open("soundbank." + in_string, "rb")
        bankPath = "banks_" + in_string
        soundPath = "sound_" + in_string
        flacPath = "flac_" + in_string
    else:
        in_file_sb.close()
        in_file_sb = open("soundbank", "rb")
    
    in_file_toc = open("toc", "rb")

    IDtables = []
    Offtables = []
    Sztables = []
    fileNameTables = []
    fileID = []
    fileIndex = []

    IDtables.append([])
    in_file_toc.seek(784880)
    for i in range(3136):
        fileID.append([])
        IDtables[0].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(812928)
    for i in range(14696):
        fileID.append([])
        IDtables[1].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(932832)
    for i in range(13748):
        fileID.append([])
        IDtables[2].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(1045136)
    for i in range(13747):
        fileID.append([])
        IDtables[3].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(1157440)
    for i in range(13747):
        fileID.append([])
        IDtables[4].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(1269744)
    for i in range(13747):
        IDtables[5].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(1382048)
    for i in range(13747):
        fileID.append([])
        IDtables[6].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(1494352)
    for i in range(13747):
        fileID.append([])
        IDtables[7].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(1606656)
    for i in range(13747):
        fileID.append([])
        IDtables[8].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(1718968)
    for i in range(13747):
        fileID.append([])
        IDtables[9].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(1831272)
    for i in range(13747):
        fileID.append([])
        IDtables[10].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(1943576)
    for i in range(13747):
        fileID.append([])
        IDtables[11].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(2055880)
    for i in range(13747):
        fileID.append([])
        IDtables[12].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(2168184)
    for i in range(13747):
        fileID.append([])
        IDtables[13].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(2280488)
    for i in range(13747):
        fileID.append([])
        IDtables[14].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(2392792)
    for i in range(13747):
        fileID.append([])
        IDtables[15].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(2505096)
    for i in range(13747):
        fileID.append([])
        IDtables[16].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        
    IDtables.append([])
    in_file_toc.seek(2617408)
    for i in range(13747):
        fileID.append([])
        IDtables[17].append(int.from_bytes(in_file_toc.read(4), "little"))
        in_file_toc.seek(4,1)
        

    for i in range(19):
        Sztables.append([])
        Offtables.append([])
        fileNameTables.append([])

    in_file_toc.seek(2727496)
    archiveName = []
    for i in range(256):
        fileIndex.append([])
        if i == int.from_bytes(b'\x4b', "little") :
            archiveName.append("wem_0")
        elif i == int.from_bytes(b'\x4c', "little") :
            archiveName.append("wem_1")
        elif i == int.from_bytes(b'\x6f', "little") :
            archiveName.append("wem_us")
        elif i == int.from_bytes(b'\x77', "little") :
            archiveName.append("wem_fr")
        elif i == int.from_bytes(b'\x79', "little") :
            archiveName.append("wem_de")
        elif i == int.from_bytes(b'\x7b', "little") :
            archiveName.append("wem_it")
        elif i == int.from_bytes(b'\x7d', "little") :
            archiveName.append("wem_jp")
        elif i == int.from_bytes(b'\x81', "little") :
            archiveName.append("wem_pl")
        elif i == int.from_bytes(b'\x85', "little") :
            archiveName.append("wem_ru")
        elif i == int.from_bytes(b'\x87', "little") :
            archiveName.append("wem_es")
        elif i == int.from_bytes(b'\x8b', "little") :
            archiveName.append("wem_br")
        elif i == int.from_bytes(b'\x8f', "little") :
            archiveName.append("wem_la")
        elif i == int.from_bytes(b'\x92', "little") :
            archiveName.append("wem_00")
        else:
            archiveName.append("")
    for i in range(340660):
        szPrep = int.from_bytes(in_file_toc.read(4), "little")
        fID = in_file_toc.read(1)
        fSelector = 0
        fName = ""
        if fID == b'\x4b':
            fSelector = 0
            fName = "wem_0"
        elif fID == b'\x4c':
            fSelector = 0
            fName = "wem_1"
        elif fID == b'\x6f':
            fSelector = 1
            fName = "wem.us"
        elif fID == b'\x77':
            fSelector = 5
            fName = "wem.fr"
        elif fID == b'\x79':
            fSelector = 6
            fName = "wem.de"
        elif fID == b'\x7b':
            fSelector = 7
            fName = "wem.it"
        elif fID == b'\x7d':
            fSelector = 8
            fName = "wem.jp"
        elif fID == b'\x81':
            fSelector = 10
            fName = "wem.pl"
        elif fID == b'\x85':
            fSelector = 12
            fName = "wem.ru"
        elif fID == b'\x87':
            fSelector = 13
            fName = "wem.es"
        elif fID == b'\x8b':
            fSelector = 15
            fName = "wem.br"
        elif fID == b'\x8f':
            fSelector = 17
            fName = "wem.la"
        elif fID == b'\x92':
            fSelector = 0
            fName = "wem_00"
        else:
            in_file_toc.seek(11,1)
            continue
        fileID[fSelector].append(int.from_bytes(fID, "little"))
        fileNameTables[fSelector].append(fName)
        Sztables[fSelector].append(szPrep)
        in_file_toc.seek(3,1)
        theOffset = int.from_bytes(in_file_toc.read(4), "little")
        Offtables[fSelector].append(theOffset)
        fileIndex[int.from_bytes(fID, "little")].append(theOffset)
        in_file_toc.seek(4,1)
    in_file_toc.close()

    checked = []
    for i in range(256):
        fileIndex[i].sort()
        checked.append([])

    #print(IDtables[1][0])
    if not os.path.exists(bankPath + os.path.sep + "wem"):
        os.makedirs(bankPath + os.path.sep + "wem")
    theCount = 0
    if in_string == "us":
        theCount = 1
    if in_string == "fr":
        theCount = 5
    if in_string == "de":
        theCount = 6
    if in_string == "it":
        theCount = 7
    if in_string == "jp":
        theCount = 8
    if in_string == "pl":
        theCount = 10
    if in_string == "ru":
        theCount = 12
    if in_string == "es":
        theCount = 13
    if in_string == "br":
        theCount = 15
    if in_string == "la":
        theCount = 17
    for i in range(len(fileNameTables[theCount])):
        in_file_wem = open(fileNameTables[theCount][i], "rb")
        out_file_wem = open(bankPath + os.path.sep + "wem" + os.path.sep + str(IDtables[theCount][i]) + ".wem", "wb")
        in_file_wem.seek(Offtables[theCount][i])
        out_file_wem.write(in_file_wem.read(Sztables[theCount][i]))
        in_file_wem.close()
        out_file_wem.close()
    in_file_sb.close()
    os.remove("tmp")

    if not os.path.exists(bankPath + os.path.sep + "wem"):
        os.makedirs(bankPath + os.path.sep + "wem")

    for file in sorted(os.listdir(bankPath)):
        if not file.endswith(".bnk"):
            continue
        shutil.copy(bankPath + os.path.sep + file, bankPath + os.path.sep + "wem" + os.path.sep + file)

    for folder in sorted(os.listdir(bankPath + os.path.sep + "txtp_sorted")):
        bankChecked = []
        if os.path.isdir(bankPath + os.path.sep + "txtp_sorted" + os.path.sep + folder):
            if not os.path.exists(flacPath + os.path.sep + folder):
                os.makedirs(flacPath + os.path.sep + folder)
            for file in sorted(os.listdir(bankPath + os.path.sep + "txtp_sorted" + os.path.sep + folder)):
                fileBase = file.split(".")[0].split("~")[0]
                print("Converting " + fileBase)
                fileProc = fr"{file}"
                print(fileProc)
                fileBaseProc = fileProc.split(".")[0]
                
                if not os.path.exists(flacPath + os.path.sep + folder + os.path.sep + fileBase):
                    os.makedirs(flacPath + os.path.sep + folder + os.path.sep + fileBase)
                if not file.endswith(".txtp"):
                    continue
                fileOpen = open(bankPath + os.path.sep + "txtp_sorted" + os.path.sep + folder + os.path.sep + file, "r")
                fileRead = fileOpen.read()
                fileOpen.close()
                if re.findall('\d+[.]wem', fileRead) != None:
                    bankDep = re.findall('\d+[.]wem', fileRead)
                    for item in range(len(bankDep)):
                        for fSelect in range(len(IDtables)):
                            if int(bankDep[item].split(".wem")[0]) in IDtables[fSelect]:
                                IDCheck = int(bankDep[item].split(".wem")[0])
                                sourceWem = ""
                                try:
                                    sourceWem = archiveName[fileID[fSelect][IDtables[fSelect].index(IDCheck)]]
                                except:
                                    continue
                                if validType == True and in_string not in sourceWem:
                                    continue
                                offCheck = Offtables[fSelect][IDtables[fSelect].index(IDCheck)]
                                wemIndex = fileIndex[fileID[fSelect][IDtables[fSelect].index(IDCheck)]].index(offCheck)
                                if wemIndex in checked[fileID[fSelect][IDtables[fSelect].index(IDCheck)]]:
                                    continue
                                metaPath = flacPath + os.path.sep + folder + os.path.sep + fileBaseProc + os.path.sep + sourceWem + '_' + str(wemIndex) + '.txt'
                                metaFile = open(metaPath, "w")
                                metaFile.write('Replace this file name base with a custom Wwise "wem" file.')
                                metaFile.close()
                bankDep = re.findall('wem/.+#s\d+', fileRead)
                for item in range(len(bankDep)):
                    subsong = fileBaseProc + "-" + bankDep[item].split("#s")[1]
                    if bankDep[item].split("#s")[1] in bankChecked:
                        continue
                    metaPath = '..' + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + flacPath + os.path.sep + folder + os.path.sep + fileBaseProc + os.path.sep + subsong + '.txt'
                    metaFile = open(metaPath, "w")
                    metaFile.write('Replace this file name base with a custom Wwise "wem" file.')
                    metaFile.close()
                    bankChecked.append(bankDep[item].split("#s")[1])
        else:
            print("Debug!")
    print("\nSuccess!")


#in_string = input("Rift Apart WWise Bank Language Suffix: ")
#toc2(in_string)
