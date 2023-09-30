import os
import shutil
import subprocess
import re

def sort(in_string, validType):
    in_file_sb = open("tmp", "wb")
    out_file_txt = open("tmp2", "w")
    if validType == True:
        in_file_sb.close()
        out_file_txt.close()
        os.remove("tmp")
        os.remove("tmp2")
        in_file_sb = open("soundbank." + in_string, "rb")
        out_file_txt = open("list." + in_string, "w")
    else:
        in_file_sb.close()
        out_file_txt.close()
        os.remove("tmp")
        os.remove("tmp2")
        in_file_sb = open("soundbank", "rb")
        out_file_txt = open("list", "w")

    in_file_sb.seek(0,2)
    sbSize = in_file_sb.tell()
    in_file_sb.seek(0)

    sbNames = []
    sNames = []
    sbStart = []
    objIDs = []
    sCounts = []
            
    in_file_sb.seek(0)
    RTableOffset = []
    objID = 0
    sCount = 0
    objIDs = []
    objNames = []
    sbNamesinBank = []
    while in_file_sb.tell() < sbSize - 1024:
        readTest = in_file_sb.read(4)
        sNamesinBank = []
        in_file_sb.seek(-4,1)
        if readTest == b'1TAD':
            sbStart.append(in_file_sb.tell())
            in_file_sb.seek(12,1)
            sizeCheck = int.from_bytes(in_file_sb.read(4), "little")
            in_file_sb.seek(sbStart[len(sbStart) - 1] + 32)
            if sizeCheck == 3:
                in_file_sb.seek(-12,1)
            NTStart = int.from_bytes(in_file_sb.read(4), "little") + sbStart[len(sbStart) - 1]
            NTEnd = int.from_bytes(in_file_sb.read(4), "little") + sbStart[len(sbStart) - 1] + NTStart
            #sb_search = in_file_sb.read(4096)
            #in_file_sb.seek(-4096, 1)
            #if sb_search.find(b'WAVEfmt') < 0:
                #continue
            in_file_sb.seek(NTStart + 12)
            sbName = ''
            sbRead = in_file_sb.read(1)
            while sbRead != b'\x00':
                sbStr = str(sbRead, 'UTF-8')
                sbName += sbStr
                sbRead = in_file_sb.read(1)
            sbNames.append(sbName.split(".")[0])
            #print(sbName)
            #print(in_file_sb.tell())
                
            sCount = 0
            sCounts.append(0)
            in_file_sb.seek(NTStart)
            while in_file_sb.tell() < NTEnd:
                sName = ""
                sRead = in_file_sb.read(1)
                if in_file_sb.tell() >= NTEnd:
                    break
                if sRead == b'\x00':
                    while sRead == b'\x00':
                        sRead = in_file_sb.read(1)
                        if in_file_sb.tell() >= NTEnd:
                            break
                if not sRead.isupper() and not sRead.islower():
                    #print("#1 : " + str(sRead))
                    break
                while sRead != b'\x00' and int.from_bytes(sRead, "little") < 123:
                    try:
                        sStr = str(sRead, 'UTF-8')
                    except:
                        break
                    sName += sStr
                    sRead = in_file_sb.read(1)
                    if in_file_sb.tell() >= NTEnd:
                        break

                #print(sName)

                if len(sName) < 6:
                    #print("#2 + " + sName)
                    #print(sbName.split(".")[0])
                    in_file_sb.seek(-1,1)
                    break
                #if sName.find("VFX_SWITCH_LOADER") >= 0:
                    #break
                #if sName.startswith("Play") == True:
                    #break
                #if sName.startswith("Stop") == True:
                    #break
                    
                sNames.append(sName)
                sNamesinBank.append(sName)
                out_file_txt.write(sName + "\n")
                #print(sName)
                sCount += 1
            sCounts[len(sCounts) - 1] = sCount
            in_file_sb.seek(sbStart[len(sbStart) - 1] + 20)
            RTableOffset = (int.from_bytes(in_file_sb.read(4), "little") + sbStart[len(sbStart) - 1])
            RTableSize = int(int.from_bytes(in_file_sb.read(4), "little") / 16)
            in_file_sb.seek(RTableOffset)
            for j in range(RTableSize):
                in_file_sb.seek(12,1)
                objID = int.from_bytes(in_file_sb.read(2), "little")
                if len(sNamesinBank) > j:
                    objIDs.append(objID)
                    objNames.append(sNamesinBank[j])
                
            in_file_sb.seek(sbStart[len(sbStart) - 1] + 8)
            finalJump = int.from_bytes(in_file_sb.read(4), "little")
            in_file_sb.seek(sbStart[len(sbStart) - 1] + finalJump - 4)
            sbNamesinBank.append(sNamesinBank)
        in_file_sb.seek(1,1)
        
    in_file_sb.seek(0)
    sbOff = 0
    RIFFOff = 0
    nameCount = 0

    bankPath = "banks"
    if validType == True:
        bankPath = "banks_" + in_string

    print(str(len(sbNames)) + " subbanks")
    print(str(len(sNames)) + " sounds")
    out_file_txt.close()

    checked = []

    for j in range(len(sbNames)):
        if sbNames[j] not in os.listdir(bankPath + os.path.sep + "txtp"):
            continue
        for i in range(len(sbNamesinBank[j])):
            #print(sbNamesinBank[j][i])
            for file in sorted(os.listdir(bankPath + os.path.sep + "txtp" + os.path.sep + sbNames[j])):
                if not file.endswith(".txtp"):
                    continue
                fileName = file.split(" ")[0].split("~")[0].split(" (")[0].split("~")[0]
                if sbNamesinBank[j][i] in fileName:
                    fileName = sbNamesinBank[j][i]
                    #Dupes = False
                    print("Extracting " + sbNamesinBank[j][i])
                    bankCheck = open(bankPath + os.path.sep + "txtp" + os.path.sep + sbNames[j] + os.path.sep + file, "r")
                    bankCheckRead = bankCheck.read()
                    bankEmbedSearch = re.search("wem/.+[.]bnk", bankCheckRead)
                    bankCheck.close()
                    if not os.path.exists(bankPath + os.path.sep + "txtp_sorted" + os.path.sep + sbNames[j]):
                        os.makedirs(bankPath + os.path.sep + "txtp_sorted" + os.path.sep + str(sbNames[j]))
                    fileOpen = open(bankPath + os.path.sep + "txtp" + os.path.sep + sbNames[j] + os.path.sep + file, "r")
                    fileRead = fileOpen.read()
                    fileOpen.close()
                    bankDeps = re.findall('[.][.]/[.][.]/+wem/.+[.]wem', fileRead)
                    if len(bankDeps) > 1:
                        for rcount in range(len(bankDeps)):
                            if ".bnk" in bankDeps[rcount]:
                                bankDeps[rcount] = bankDeps[rcount].split(" ")[0] + " " + bankDeps[rcount].split(" ")[1]
                            if os.system == 'win32' or os.system == 'win64':
                                bankDeps[rcount] = bankDeps[rcount].replace("/", "\\")
                            if bankDeps[rcount] in checked:
                                continue
                            offset = 1
                            if os.path.exists(bankPath + os.path.sep + 'txtp_sorted' + os.path.sep + sbNames[j] + os.path.sep + fileName + '_' + str(rcount + offset) + '.txtp'):
                                while os.path.exists(bankPath + os.path.sep + 'txtp_sorted' + os.path.sep + sbNames[j] + os.path.sep + fileName + '_' + str(rcount + offset) + '.txtp'):
                                    offset += 1
                            os.system('echo ' + bankDeps[rcount] + ' > "' + bankPath + os.path.sep + 'txtp_sorted' + os.path.sep + sbNames[j] + os.path.sep + fileName + '_' + str(rcount + offset) + '.txtp"')
                            checked.append(bankDeps[rcount])
                    elif len(bankDeps) == 1:
                        if ".bnk" in bankDeps[0]:
                            bankDeps[0] = bankDeps[0].split(" ")[0] + " " + bankDeps[0].split(" ")[1]
                        if os.system == 'win32' or os.system == 'win64':
                            bankDeps[rcount] = bankDeps[rcount].replace("/", "\\")
                        if bankDeps[0] in checked:
                            continue
                        offset = 1
                        if os.path.exists(bankPath + os.path.sep + 'txtp_sorted' + os.path.sep + sbNames[j] + os.path.sep + fileName + '_' + str(offset) + '.txtp'):
                            while os.path.exists(bankPath + os.path.sep + 'txtp_sorted' + os.path.sep + sbNames[j] + os.path.sep + fileName + '_' + str(offset) + '.txtp'):
                                offset += 1
                            fileName += "_" + str(offset)
                        os.system('echo ' + bankDeps[0] + ' > "' + bankPath + os.path.sep + 'txtp_sorted' + os.path.sep + sbNames[j] + os.path.sep + fileName + '.txtp"')
                        checked.append(bankDeps[0])
                    #Dupes = True
                    
    in_file_sb.close()
    if validType == True:
        os.remove("list." + in_string)
    else:
        os.remove("list")


#in_string = input("Rift Apart WWise Bank Language Suffix: ")
#sort(in_string)
