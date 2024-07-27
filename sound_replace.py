import os, re, struct, shutil, sys

def run(bank_name):
    shutil.copy(bank_name + ".soundbank_vanilla", bank_name + ".soundbank")
    bank = open(bank_name + ".soundbank", "rb+")
    bank.seek(0,2)
    bankSize = bank.tell()

    tracks = []
    trackData = []
    trackList = []
    segments = []
    segmentData = []
    segmentList = []
    autoList = []
    autoData = []
    checked = []
    normalizeList = []
    sounds = []
    soundData = []
    soundList = []
    for file in sorted(os.listdir("txtp" + os.path.sep + bank_name)):
        if file.endswith(".txtp"):
            txtp = open("txtp" + os.path.sep + bank_name + os.path.sep + file, "r")
            txtpRead = txtp.read()
            txtp.close()
            listFind = re.findall('wem/.+', txtpRead)

            soundPrep = re.findall('CAkSound[\\[]\\d+[\\]]\\s+(\\d+)', txtpRead)
            for count in range(len(soundPrep)):
                soundList.append(int(soundPrep[count]))

            segmentPrep = re.findall('CAkMusicSegment[\\[]\\d+[\\]]\\s+(\\d+)', txtpRead)
            for count in range(len(segmentPrep)):
                segmentList.append(int(segmentPrep[count]))

            trackPrep = re.findall('CAkMusicTrack[\\[]\\d+[\\]]\\s+(\\d+)', txtpRead)
            for count in range(len(trackPrep)):
                trackList.append(int(trackPrep[count]))
                

            soundOff = []
            soundFind = re.findall('CAkSound[\\[]\\d+[\\]]\\s+(\\d+)', txtpRead)
            if len(soundFind) > 0:
                for count in range(len(soundFind)):
                    soundOff.append(txtpRead.find(soundFind[count]))
                for count in range(len(soundFind)):
                    resultLength = txtpRead[soundOff[count]:]
                    resultLength = resultLength.split(" ")[1]
                    sounds.append(soundFind[count])
                    soundData.append((txtpRead[soundOff[count]:].split("\n#\n#\n")[0]).split("CAk")[0])
            
            segmentFind = re.findall('CAkMusicSegment[\\[]\\d+[\\]]\\s+\\d+', txtpRead)
            if len(segmentFind) <= 0:
                continue
            segmentOff = []
            for count in range(len(segmentFind)):
                segmentOff.append(txtpRead.find(segmentFind[count]))
            for count in range(len(segmentFind)):
                resultLength = txtpRead[segmentOff[count]:]
                resultLength = resultLength.split(" ")[1].split("\n#\n")[0]
                segments.append(resultLength)
                segmentData.append(txtpRead[segmentOff[count]:])
                        
            trackFind = re.findall('CAkMusicTrack[\\[]\\d+[\\]]\\s+\\d+', txtpRead)
            if len(trackFind) <= 0:
                continue
            trackOff = []
            for count in range(len(trackFind)):
                trackOff.append(txtpRead.find(trackFind[count]))
            autoFind = -1
            for count in range(len(trackFind)):
                resultLength = txtpRead[trackOff[count]:]
                resultLength = resultLength.split(" ")[1]
                if resultLength.count('CAkMusicTrack') > 1:
                    resultLength = 'CAkMusicTrack' + resultLength.split('CAkMusicTrack')[1]
                if 'CAkMusicSegment' in resultLength:
                    resultLength = resultLength.split('CAkMusicSegment')[0]
                if 'AkMusicRanSeqPlaylistItem' in resultLength:
                    resultLength = resultLength.split('AkMusicRanSeqPlaylistItem')[0]
                tracks.append(resultLength)
                trackData.append(txtpRead[trackOff[count]:])
            for count in range(len(listFind)):
                if '#m0' in listFind[count]:
                    for count2 in range(len(trackOff)):
                        autoData.append(int(trackFind[count2].split("\n")[0].split("] ")[1]))
                        autoSearch = txtpRead[trackOff[count2]:]
                        if count2 < len(trackOff) - 1:
                            autoSearch = txtpRead[trackOff[count2]:trackOff[count2+1]]
                        if ('# automations: 1' in autoSearch or '# automations: 2' in autoSearch) and int(trackFind[count2].split("\n")[0].split("] ")[1]) not in checked:
                            normalizeFind = re.findall('# normalize: (\\d+[.]+\\d+)', autoSearch)
                            if len(normalizeFind) == 0:
                                continue
                            normalizeList.append(int(trackFind[count2].split("\n")[0].split("] ")[1]))
                            normalizeList.append(int(float(normalizeFind[0]) * 1000000))
                            autoList = re.findall('#m0^\\d+[.]+\\d+\\~\\d+[.]+\\d+\\=[A-Z]@-1\\~\\d+[.]+\\d+\\+\\d+[.]+\\d+\\~-1', listFind[count])
                            autoData.append(len(autoList) + 1)
                            autoTime = 0
                            for count3 in range(len(autoList)):
                                if count3 == 0:
                                        autoData.append(float(autoList[count3].split('^')[1].split('~')[0]))
                                        autoTime = float(autoList[count3].split('~')[2].split('+')[0])
                                        autoData.append(autoTime)
                                autoData.append(float(autoList[count3].split('~')[1].split('=')[0]))
                                autoTime = float(autoList[count3].split('~')[2].split('+')[0]) + float(autoList[count3].split('+')[1].split('~')[0])
                                autoData.append(autoTime)
                            checked.append(int(trackFind[count2].split("\n")[0].split("] ")[1]))
                            break
                        else:
                            autoData.append(0)
            

    bank.seek(0)
    HIRCStart = 0
    while bank.tell() < bankSize - 32768:
        bankStart = bank.tell()
        bankRead = bank.read(65536)
        if b'HIRC' in bankRead:
            HIRCStart = bankStart + bankRead.find(b'HIRC')
    bank.seek(HIRCStart + 4)
    HIRCSize = int.from_bytes(bank.read(4), "little")
    HIRCCount = int.from_bytes(bank.read(4), "little")
    for i in range(HIRCCount - 32):
        CurrOff = bank.tell()
        HIRCItem = int.from_bytes(bank.read(1), "little")
        HIRCItemSize = int.from_bytes(bank.read(4), "little")
        if HIRCItem != 10 and HIRCItem != 11 and HIRCItem != 2:
            bank.seek(HIRCItemSize,1)
        if HIRCItem == 2:
            HIRCItemData = bank.read(HIRCItemSize)
            IDA = int.from_bytes(HIRCItemData[:4], "little")
            for j in range(len(sounds)):
                soundCheck = int(sounds[j].split("\n")[0])
                if soundCheck == IDA:
                    soundSourceCheck = int((soundData[j].split("Source ")[1]).split("\n")[0]).to_bytes(4, "little")
                    if soundSourceCheck != int.from_bytes(HIRCItemData[9:13], "little"):
                        bank.seek(CurrOff + 13)
                        bank.write(b'\x01')
                        bank.write(soundSourceCheck)
                        print("Sound " + str(int.from_bytes(HIRCItemData[9:13], "little")) + " replaced with " + str(int.from_bytes(soundSourceCheck, "little")) + "!")
                
        if HIRCItem == 10:
            HIRCItemData = bank.read(HIRCItemSize)
            IDA = int.from_bytes(HIRCItemData[:4], "little")
            #if IDA not in segmentList:
                #bank.seek(CurrOff + HIRCItemSize + 5)
                #continue
            for j in range(len(segments)):
                segCheck = int(segments[j].split("\n")[0]).to_bytes(4, "little")
                if segCheck == HIRCItemData[:4]:
                    
                    fVolume = 0
                    bank.seek(CurrOff + 22)
                    propCheck = int.from_bytes(bank.read(1), "little")
                    if propCheck > 0:
                        volumeProp = 0
                        for iteration in range(propCheck):
                            propCheck2 = int.from_bytes(bank.read(1), "little")
                            if propCheck2 == 1:
                                volumeProp = iteration
                        for iter2 in range(volumeProp):
                            bank.seek(4,1)
                        fVolumeFinds = re.findall('Volume:\\s+([-]?\\d+[.]?\\d*)',segmentData[j])
                        if len(fVolumeFinds) > 0:
                            fVolume = float(fVolumeFinds[0])
                            bank.write(struct.pack('<f', float(fVolume)))
                            
                    bank.seek(CurrOff + 5)
                    fDuration = float(segmentData[j][segmentData[j].find('fDuration: ') + 11:].split('\n')[0])
                    fEndMark = re.findall('AkMusicMarkerWwise:\\s+(\\d+[.]?\\d*)',segmentData[j])
                    offFix = HIRCItemData.find(b'\x42\x04\x04\x00')
                    offFix2 = HIRCItemData.find(b'\x42\x04\x04\x01')
                    offFix3 = HIRCItemData.find(b'\x43\x04\x04\x00')
                    offFix4 = HIRCItemData.find(b'\x43\x04\x04\x01')
                    if offFix > 0:
                        bank.seek(CurrOff + offFix + 13)
                        bank.write(struct.pack('<d', fDuration))
                        bank.seek(CurrOff + offFix + 29)
                        bank.write(struct.pack('<d', float(fEndMark[0])))
                        bank.seek(CurrOff + offFix + 45)
                        bank.write(struct.pack('<d', float(fEndMark[1])))
                    elif offFix2 > 0:
                        bank.seek(CurrOff + offFix2 + 13)
                        bank.write(struct.pack('<d', fDuration))
                        bank.seek(CurrOff + offFix2 + 29)
                        bank.write(struct.pack('<d', float(fEndMark[0])))
                        bank.seek(CurrOff + offFix2 + 45)
                        bank.write(struct.pack('<d', float(fEndMark[1])))
                    elif offFix3 > 0:
                        bank.seek(CurrOff + offFix3 + 13)
                        bank.write(struct.pack('<d', fDuration))
                        bank.seek(CurrOff + offFix3 + 29)
                        bank.write(struct.pack('<d', float(fEndMark[0])))
                        bank.seek(CurrOff + offFix3 + 45)
                        bank.write(struct.pack('<d', float(fEndMark[1])))
                    elif offFix4 > 0:
                        bank.seek(CurrOff + offFix4 + 13)
                        bank.write(struct.pack('<d', fDuration))
                        bank.seek(CurrOff + offFix4 + 29)
                        bank.write(struct.pack('<d', float(fEndMark[0])))
                        bank.seek(CurrOff + offFix4 + 45)
                        bank.write(struct.pack('<d', float(fEndMark[1])))
                    else:
                        print("Address later!")
        if HIRCItem == 11:
            HIRCItemData = bank.read(HIRCItemSize)
            IDB = int.from_bytes(HIRCItemData[:4], "little")
            if IDB not in trackList:
                bank.seek(CurrOff + HIRCItemSize + 5)
                continue
            for j in range(len(tracks)):
                trackCheck = (int(tracks[j].split("\n")[0])).to_bytes(4, "little")
                if trackCheck == HIRCItemData[:4]:
                    bank.seek(CurrOff + 10)
                    numSubTrack = int.from_bytes(bank.read(1), "little")
                    bank.seek(CurrOff + 22)
                    for k in range(numSubTrack):
                        bank.seek(14,1)
                    for k in range(numSubTrack):
                        IDCheck = int.from_bytes(bank.read(4),"little")
                        sourceID = int(trackData[j][trackData[j].find('sourceID: ') + 10:].split('\n')[0])
                        if IDCheck != sourceID:
                            bank.seek(-4,1)
                            bank.write(sourceID.to_bytes(4,"little"))
                            stamp = bank.tell()
                            bank.seek(CurrOff + 19 + (14 * k))
                            bank.write(sourceID.to_bytes(4,"little"))
                            bank.seek(stamp)
                            print("Music " + str(IDCheck) + " replaced with " + str(sourceID) + "!")
                        bank.seek(4,1)
                        fPlayAt = float(trackData[j][trackData[j].find('fPlayAt: ') + 9:].split('\n')[0])
                        bank.write(struct.pack('<d', fPlayAt))
                        fBeginTrimOffset = float(trackData[j][trackData[j].find('fBeginTrimOffset: ') + 18:].split('\n')[0])
                        bank.write(struct.pack('<d', fBeginTrimOffset))
                        fEndTrimOffset = float(trackData[j][trackData[j].find('fEndTrimOffset: ') + 16:].split('\n')[0])
                        bank.write(struct.pack('<d', fEndTrimOffset))
                        fSrcDuration = float(trackData[j][trackData[j].find('fSrcDuration: ') + 14:].split('\n')[0])
                        bank.write(struct.pack('<d', fSrcDuration))
                        bank.seek(4,1)
                        numAutos = int.from_bytes(bank.read(4), "little")
                        if (numAutos == 1 or numAutos == 2) and IDB in normalizeList:
                            autoCheck = autoData.index(int.from_bytes(trackCheck, "little"))
                            bank.seek(8,1)
                            numAutoSteps = int.from_bytes(bank.read(4), "little")
                            theCounter = 0
                            normalizeIndex = normalizeList.index(IDB)
                            for n in range(numAutoSteps):
                                if autoData[autoCheck + 1] > numAutoSteps:
                                    break
                                [fTimeIn] = struct.unpack('f',bank.read(4))
                                [fValIn] = struct.unpack('f',bank.read(4))
                                fCurveType = int.from_bytes(bank.read(4),"little")
                                if fCurveType == 9:
                                    print("Fixme")
                                    continue

                                fValOut = min(1.0,max(0.0,((normalizeList[normalizeIndex + 1]) / 1000000.0)))
                                if fValIn <= 0:
                                    fValOut -= 1.0
                                    
                                bank.seek(-8,1)
                                bank.write(struct.pack('<f',fValOut))
                                bank.seek(4,1)

                                theCounter += 1
                            
        bank.seek(CurrOff + HIRCItemSize + 5)
        
    bank.close()
    print("Done!")


if len(sys.argv) > 1:
    run(sys.argv[1])
else:
    print("Nothing done.")
    print("Specify a WWise soundbank without the extension.")
    print("An unmodifed copy with extension \"soundbank_vanilla\" should already exist!")
