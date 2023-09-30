import os
import shutil
import subprocess
import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def toc(in_string):
    validType = in_string == "us" or in_string == "br"
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
        elif i == int.from_bytes(b'\x8b', "little") :
            archiveName.append("wem_br")
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
        elif fID == b'\x8b':
            fSelector = 15
            fName = "wem.br"
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
    if not os.path.exists(bankPath + os.sep + "wem"):
        os.makedirs(bankPath + os.sep + "wem")
    theCount = 0
    if in_string == "us":
        theCount = 1
    if in_string == "br":
        theCount = 15
    for i in range(len(fileNameTables[theCount])):
        in_file_wem = open(fileNameTables[theCount][i], "rb")
        out_file_wem = open(bankPath + os.sep + "wem" + os.sep + str(IDtables[theCount][i]) + ".wem", "wb")
        in_file_wem.seek(Offtables[theCount][i])
        out_file_wem.write(in_file_wem.read(Sztables[theCount][i]))
        in_file_wem.close()
        out_file_wem.close()
    in_file_sb.close()
    os.remove("tmp")

    if not os.path.exists(bankPath + os.sep + "wem"):
        os.makedirs(bankPath + os.sep + "wem")

    for file in sorted(os.listdir(bankPath)):
        if not file.endswith(".bnk"):
            continue
        shutil.copy(bankPath + os.sep + file, bankPath + os.sep + "wem" + os.sep + file)

    for folder in sorted(os.listdir(bankPath + os.sep + "txtp_sorted")):
        bankChecked = []
        if os.path.isdir(bankPath + os.sep + "txtp_sorted" + os.sep + folder):
            if not os.path.exists(flacPath + os.sep + folder):
                os.makedirs(flacPath + os.sep + folder)
            for file in sorted(os.listdir(bankPath + os.sep + "txtp_sorted" + os.sep + folder)):
                fileBase = file.split(".")[0].split("~")[0]
                print("Converting " + fileBase)
                fileProc = file.replace(" ","\ ")
                fileProc = fileProc.replace("(","\(").replace(")","\)")
                fileProc = fileProc.replace("{","\{").replace("}","\}")
                fileProc = fileProc.replace("[","\[").replace("]","\]")
                fileBaseProc = fileProc.split(".")[0].split("~")[0]
                
                if not os.path.exists(flacPath + os.sep + folder + os.sep + fileBase):
                    os.makedirs(flacPath + os.sep + folder + os.sep + fileBase)
                if not file.endswith(".txtp"):
                    continue
                fileOpen = open(bankPath + os.sep + "txtp_sorted" + os.sep + folder + os.sep + file, "r")
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
                                os.chdir(bankPath + os.sep + "txtp_sorted" + os.sep + folder)
                                os.system("vgmstream-cli -D 2 -i -o " + ".." + os.sep + ".." + os.sep + ".." + os.sep + flacPath + os.sep + folder + os.sep + fileBaseProc + os.sep + sourceWem + "_" + str(wemIndex) + ".wav " + fileProc + " > .." + os.sep + ".." + os.sep + ".." + os.sep + "vgmstream.log")
                                os.chdir(".." + os.sep + ".." + os.sep + "..")
                                checked[fileID[fSelect][IDtables[fSelect].index(IDCheck)]].append(wemIndex)
                bankDep = re.findall('wem' + os.sep + '.+#s\d+', fileRead)
                for item in range(len(bankDep)):
                    subsong = fileBaseProc + "-" + bankDep[item].split("#s")[1]
                    if bankDep[item].split("#s")[1] in bankChecked:
                        continue
                    os.chdir(bankPath + os.sep + "txtp_sorted" + os.sep + folder)
                    os.system("vgmstream-cli -D 2 -i -o " + ".." + os.sep + ".." + os.sep + ".." + os.sep + flacPath + os.sep + folder + os.sep + fileBaseProc + os.sep + subsong + ".wav " + fileProc + " > .." + os.sep + ".." + os.sep + ".." + os.sep + "vgmstream.log")
                    os.chdir(".." + os.sep + ".." + os.sep + "..")
                    bankChecked.append(bankDep[item].split("#s")[1])
                        
                for file2 in sorted(os.listdir(flacPath + os.sep + folder + os.sep + fileBase)):
                    if not file2.endswith(".wav"):
                        continue
                    fileBase2 = file2.split(".")[0].split("~")[0]
                    parent = ""
                    if not file2.startswith("wem"):
                        parent = ".." + os.sep
                    os.system("ffmpeg -y -loglevel quiet -i " + flacPath + os.sep + folder + os.sep + fileBaseProc + os.sep + file2 + " " + flacPath + os.sep + folder + os.sep + fileBaseProc + os.sep + parent + fileBase2 + ".flac")
                    os.remove(flacPath + os.sep + folder + os.sep + fileBase + os.sep + file2)
                for file3 in sorted(os.listdir(flacPath + os.sep + folder)):
                    if os.path.isdir(flacPath + os.sep + folder + os.sep + file3) and len(os.listdir(flacPath + os.sep + folder + os.sep + file3)) == 0:
                        os.system("rm -rf " + flacPath + os.sep + folder + os.sep + file3)
        else:
            print("Debug!")
    print("\nSuccess!")


#in_string = input("Rift Apart WWise Bank Language Suffix: ")
#toc2(in_string)
