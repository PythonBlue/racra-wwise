import os
import shutil
import subprocess
import re
def names(in_string):
    in_file_sb = open("tmp", "wb")
    bankPath = "banks"
    if in_string == "us" or in_string == "br":
        in_file_sb.close()
        in_file_sb = open("soundbank." + in_string, "rb")
        bankPath = "banks_" + in_string
    else:
        in_file_sb.close()
        in_file_sb = open("soundbank", "rb")

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
            NTEnd = int.from_bytes(in_file_sb.read(4), "little")
            #sb_search = in_file_sb.read(4096)
            #in_file_sb.seek(-4096, 1)
            #if sb_search.find(b'WAVEfmt') < 0:
                #continue
            in_file_sb.seek(NTStart + 12)
            sbName = ''
            sbRead = in_file_sb.read(1)
            NTCount = 1
            while sbRead != b'\x00':
                sbStr = str(sbRead, 'UTF-8')
                sbName += sbStr
                sbRead = in_file_sb.read(1)
                NTCount += 1
            sbNames.append(sbName.split(".")[0])
            print(sbName)
                
            sCount = 0
            sCounts.append(0)
            if not os.path.exists(bankPath + os.sep + "wwnames"):
                os.makedirs(bankPath + os.sep + "wwnames")
            out_file_txt = open(bankPath + os.sep + "wwnames" + os.sep + sbName.split(".sound")[0] + ".txt", "w")
            
            while NTCount < NTEnd - 8:
                sName = ''
                sRead = in_file_sb.read(1)
                NTCount += 1
                if sRead == b'\x00':
                    continue
                if not sRead.isalpha():
                    break
                while sRead != b'\x00' and int.from_bytes(sRead, "little") < 123:
                    try:
                        sStr = str(sRead, 'UTF-8')
                    except:
                        break
                    sName += sStr
                    sRead = in_file_sb.read(1)
                    NTCount += 1

                if len(sName) < 4 or NTCount > NTEnd - 8:
                    in_file_sb.seek(-1,1)
                    break
                #if sName.find("VFX_SWITCH_LOADER") >= 0:
                    #break
                #if sName.startswith("Play") == True:
                    #break
                #if sName.startswith("Stop") == True or sName.startswith("STOP") == True:
                    #continue
                    
                sNames.append(sName)
                sNamesinBank.append(sName)
                out_file_txt.write(sName + "\n")
                #print(sName)
                sCount += 1
            out_file_txt.close()
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
    in_file_sb.close()
    os.remove("tmp")
    
#in_string = input("Rift Apart WWise Bank Language Suffix: ")
#names(in_string)
