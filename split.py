import os
import shutil

def split(in_string):
    in_file_sb = open("tmp", "wb")
    if in_string == "us" or in_string == "br":
        in_file_sb.close()
        in_file_sb = open("soundbank." + in_string, "rb")
    else:
        in_file_sb.close()
        in_file_sb = open("soundbank", "rb")
    os.remove("tmp")

    in_file_sb.seek(0,2)
    sbSize = in_file_sb.tell()
    in_file_sb.seek(0)

    sbNames = []
    sNames = []
    sNamesinBank = []
    sbStart = []
    objIDs = []
    sCounts = []
    sbSizes = []

    while in_file_sb.tell() < sbSize - 512:
        readTest = in_file_sb.read(256)
        if readTest.find(b'1TAD') == -1:
            continue
        in_file_sb.seek(readTest.find(b'1TAD') - 256, 1)
        readTest2 = in_file_sb.read(256)
        in_file_sb.seek(-256,1)
        if readTest2.find(b'1TAD', 8) > -1:
            in_file_sb.seek(8,1)
            continue
        sNamesSorted = []
        sNamesinBank.append(0)
        sbStart.append(in_file_sb.tell())
        in_file_sb.seek(8,1)
        sbSizes.append(int.from_bytes(in_file_sb.read(4), "little"))
        sizeCheck = int.from_bytes(in_file_sb.read(4), "little")
        
        in_file_sb.seek(sbStart[len(sbStart) - 1] + 32)
        if sizeCheck == 3:
            in_file_sb.seek(-12,1)
        NTStart = int.from_bytes(in_file_sb.read(4), "little") + sbStart[len(sbStart) - 1]
        NTEnd = int.from_bytes(in_file_sb.read(4), "little")
        in_file_sb.seek(NTStart + 12)
        sbName = ''
        sbRead = in_file_sb.read(1)
        NTCount = 0
        while sbRead != b'\x00':
            sbStr = str(sbRead, 'UTF-8')
            sbName += sbStr
            sbRead = in_file_sb.read(1)
            NTCount += 1
        sbNames.append(sbName.split(".")[0])
        print(sbName)
        
        sCount = 0
        sCounts.append(0)
        
        while NTCount < NTEnd - 8:
            sName = ''
            sRead = in_file_sb.read(1)
            NTCount += 1
            if sRead == b'\x00':
                continue
            if not sRead.isupper():
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
            #if sName.startswith("Stop") == True:
            #break
                
            sNamesSorted.append(sName)
            #print(sName)
            sCount += 1
        sNamesSortedB = sorted(sNamesSorted, reverse=True)
        for i in range(len(sNamesSortedB)):
            sNames.append(sNamesSorted[i])
            sNamesinBank[len(sNamesinBank) - 1] += 1
        sCounts[len(sCounts) - 1] = sCount
    sExport = 0
    for i in range(len(sbNames)):
        if in_string != "":
            if not os.path.exists("banks_" + in_string):
                os.makedirs("banks_" + in_string)
            if os.path.exists("banks_" + in_string + os.sep + sbNames[i] + ".bnk"):
                continue
        else:
            if not os.path.exists("banks"):
                os.makedirs("banks")
            if os.path.exists("banks" + os.sep + sbNames[i] + ".bnk"):
                continue
        nameStart = sExport
        in_file_sb.seek(sbStart[i])
        prepBankRead = in_file_sb.read(sbSizes[i])
        bankSearch = prepBankRead.find(b'BKHD')
        in_file_sb.seek(sbStart[i] + bankSearch)
        wholeBank = in_file_sb.read(sbSizes[i] - bankSearch)

        out_bank = open("2", "w")
        if in_string == "us" or in_string == "br":
            out_bank.close()
            out_bank = open("banks_" + in_string + os.sep + sbNames[i] + ".bnk", "wb")
        else:
            out_bank.close()
            out_bank = open("banks" + os.sep + sbNames[i] + ".bnk", "wb")
        os.remove("2")
        
        out_bank.write(wholeBank)
        out_bank.close()
        sExport = nameStart + sNamesinBank[i]

    in_file_sb.close()

#in_string = input("Rift Apart WWise Bank Language Suffix: ")
#split(in_string)
