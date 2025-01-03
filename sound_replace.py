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
    checked = []
    normalizeList = []
    sounds = []
    soundData = []
    soundList = []
    MusicRanSeqs = []
    MusicRanSeqData = []
    MusicRanSeqList = []
    for file in sorted(os.listdir("txtp" + os.path.sep + bank_name)):
        if file.endswith(".txtp"):
            txtp = open("txtp" + os.path.sep + bank_name + os.path.sep + file, "r")
            txtpRead = txtp.read()
            txtp.close()
            listFind = re.findall('wem/.+', txtpRead)

            soundPrep = re.findall('CAkSound[\\[]\\d+[\\]]\\s+(\\d+)', txtpRead)
            for count in range(len(soundPrep)):
                soundList.append(int(soundPrep[count]))

            MusicRanSeqPrep = re.findall('CAkMusicRanSeqCntr[\\[]\\d+[\\]]\\s+(\\d+)', txtpRead)
            for count in range(len(MusicRanSeqPrep)):
                MusicRanSeqList.append(int(MusicRanSeqPrep[count]))

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
            
            MusicRanSeqOff = []
            MusicRanSeqFind = re.findall('CAkMusicRanSeqCntr[\\[]\\d+[\\]]\\s+(\\d+)', txtpRead)
            if len(MusicRanSeqFind) > 0:
                for count in range(len(MusicRanSeqFind)):
                    MusicRanSeqOff.append(txtpRead.find(MusicRanSeqFind[count]))
                for count in range(len(MusicRanSeqFind)):
                    resultLength = txtpRead[MusicRanSeqOff[count]:]
                    resultLength = resultLength.split(" ")[1]
                    MusicRanSeqs.append(MusicRanSeqFind[count])
                    MusicRanSeqData.append((txtpRead[MusicRanSeqOff[count]:].split("\n#\n#\n")[0]).split("CAk")[0].split("AkMusic")[0])
            
    bank.seek(0)
    HIRCStart = 0
    while bank.tell() < bankSize - 256:
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
        if HIRCItem == 2:
            HIRCItemData = bank.read(HIRCItemSize)
            IDA = int.from_bytes(HIRCItemData[:4], "little")
            for j in range(len(sounds)):
                soundCheck = int(sounds[j].split("\n")[0])
                if soundCheck == IDA:
                    bank.seek(CurrOff + 9)
                    #formatCheck = int((soundData[j].split("ulPluginID: 0x")[1]).split(" ")[0]).to_bytes(4, "little")
                    formatCheckPrep = (soundData[j].split("ulPluginID: 0x")[1]).split(" ")[0]
                    formatCheck = int(formatCheckPrep[0]) << 28
                    formatCheck += int(formatCheckPrep[1]) << 24
                    formatCheck += int(formatCheckPrep[2]) << 20
                    formatCheck += int(formatCheckPrep[3]) << 16
                    formatCheck += int(formatCheckPrep[4]) << 12
                    formatCheck += int(formatCheckPrep[5]) << 8
                    formatCheck += int(formatCheckPrep[6]) << 4
                    formatCheck += int(formatCheckPrep[7])
                    if formatCheck != int.from_bytes(HIRCItemData[4:8], "little"):
                        if formatCheck == 262145:
                            bank.seek(CurrOff + 9)
                            bank.write(b'\x01\x00\x04\x00')
                            print("Sound " + str(int.from_bytes(HIRCItemData[9:13], "little")) + " format now Vorbis!")
                        elif formatCheck == 1245185:
                            bank.seek(CurrOff + 9)
                            bank.write(b'\x01\x00\x13\x00')
                            print("Sound " + str(int.from_bytes(HIRCItemData[9:13], "little")) + " format now Opus!")
                
                    bank.seek(CurrOff + 13)
                    soundTypeCheck = int((soundData[j].split("StreamType: 0x0")[1]).split(" ")[0]).to_bytes(1, "little")
                    if soundTypeCheck != HIRCItemData[8].to_bytes(1,"little") and soundTypeCheck == b'\x02':
                        bank.seek(CurrOff + 13)
                        bank.write(soundTypeCheck)
                        print("Sound " + str(int.from_bytes(HIRCItemData[9:13], "little")) + " now streamed!")
                
                    bank.seek(CurrOff + 14)
                    soundSourceCheck = int((soundData[j].split("Source ")[1]).split("\n")[0]).to_bytes(4, "little")
                    if soundSourceCheck != HIRCItemData[9:13]:
                        bank.seek(CurrOff + 13)
                        bank.write(b'\x02')
                        bank.write(soundSourceCheck)
                        print("Sound " + str(int.from_bytes(HIRCItemData[9:13], "little")) + " replaced with " + str(int.from_bytes(soundSourceCheck, "little")) + "!")
                    
        elif HIRCItem == 10:
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
                            if propCheck2 == 0:
                                volumeProp = iteration
                                bank.seek(CurrOff + 23 + propCheck)
                                break
                        for iter2 in range(volumeProp):
                            bank.seek(4,1)
                        fVolumeFinds = re.findall('\\* \\[Volume\\]:\\s+([-]?\\d+[.]?\\d*)',segmentData[j])
                        if len(fVolumeFinds) > 0:
                            fVolume = float(fVolumeFinds[0])
                            outputOff = struct.unpack('f',bank.read(4))
                            if fVolume != outputOff:
                                bank.seek(-4,1)
                                bank.write(struct.pack('<f', float(fVolume)))
                                print("Music Segment " + str(IDA) + " attenuated!")
                            
                    bank.seek(CurrOff + 5)
                    fTempo = 0
                    uTimeSigNumBeatsBar = 0
                    uTimeSigBeatValue = 0
                    if segmentData[j].find('fTempo: ') > 0:
                        fTempo = float(segmentData[j][segmentData[j].find('fTempo: ') + 8:].split('\n')[0])
                    if segmentData[j].find('uTimeSigNumBeatsBar: ') > 0 and segmentData[j].find('uTimeSigBeatValue: ') > 0:
                        uTimeSigNumBeatsBar = int(re.findall('uTimeSigNumBeatsBar:\\s(\\d+)', segmentData[j])[0])
                        uTimeSigBeatValue = int(re.findall('uTimeSigBeatValue:\\s(\\d+)', segmentData[j])[0])
                        if uTimeSigBeatValue != 2 and uTimeSigBeatValue != 4 and uTimeSigBeatValue != 8 and uTimeSigBeatValue != 16:
                            uTimeSigNumBeatsBar = 0
                            uTimeSigBeatValue = 0
                    fDuration = float(segmentData[j][segmentData[j].find('fDuration: ') + 11:].split('\n')[0])
                    fEndMark = re.findall('AkMusicMarkerWwise:\\s+(\\d+[.]?\\d*)',segmentData[j])
                    offFix = HIRCItemSize - 50
                    if offFix > 0:
                        bank.seek(CurrOff + offFix)
                        if fTempo > 0:
                            bank.write(struct.pack('<f', fTempo))
                        bank.seek(CurrOff + offFix + 4)
                        if uTimeSigNumBeatsBar > 0 and uTimeSigBeatValue > 0:
                            bank.write(uTimeSigNumBeatsBar.to_bytes(1,"little"))
                            bank.write(uTimeSigBeatValue.to_bytes(1,"little"))
                        bank.seek(CurrOff + offFix + 11)
                        bank.write(struct.pack('<d', fDuration))
                        bank.seek(CurrOff + offFix + 27)
                        bank.write(struct.pack('<d', float(fEndMark[0])))
                        bank.seek(CurrOff + offFix + 43)
                        bank.write(struct.pack('<d', float(fEndMark[1])))
                    else:
                        print("Address later!")
        elif HIRCItem == 11:
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
                    bank.seek(CurrOff + 14)
                    for k in range(numSubTrack):
                        ulPluginIDIn = int.from_bytes(bank.read(4), "little")
                        ulPluginIDOut = int(re.findall('ulPluginID\\: 0x(\\d+)', trackData[j])[k])
                        if ulPluginIDIn != ulPluginIDOut:
                            if ulPluginIDOut == 262145 or ulPluginIDOut == 1245185:
                                bank.seek(-4,1)
                                bank.write(ulPluginIDOut.to_bytes(4,"little"))
                                if ulPluginIDOut == 262145:
                                    print("Format changed to Vorbis!")
                                else:
                                    print("Format changed to Opus!")
                        StreamTypeIn = int.from_bytes(bank.read(1), "little")
                        StreamTypeOut = int(re.findall('StreamType\\: 0x(\\d+)', trackData[j])[k])
                        if StreamTypeIn != StreamTypeOut:
                            if StreamTypeOut == 2:
                                bank.seek(-1,1)
                                bank.write(StreamTypeOut.to_bytes(1,"little"))
                                print("Sound now streamed!")
                        IDCheck = int.from_bytes(bank.read(4),"little")
                        sourceID = int(re.findall('sourceID\\: (\\d+)', trackData[j])[k])
                        if IDCheck != sourceID:
                            bank.seek(-4,1)
                            bank.write(sourceID.to_bytes(4,"little"))
                        bank.seek(5,1)
                    playlistItems = int.from_bytes(bank.read(1), "little")
                    bank.seek(CurrOff + 22 + (14 * numSubTrack))
                    print(playlistItems)
                    print(bank.tell())
                    for k in range(playlistItems):
                        IDCheck = int.from_bytes(bank.read(4),"little")
                        if IDCheck == 0:
                            break
                        sourceID = int(re.findall('sourceID\\: (\\d+)', trackData[j])[k])
                        if IDCheck != sourceID:
                            bank.seek(-4,1)
                            bank.write(sourceID.to_bytes(4,"little"))
                            print("Music " + str(IDCheck) + " replaced with " + str(sourceID) + "!")
                        bank.seek(4,1)
                        fPlayAt = float(re.findall('fPlayAt\\: ([-]?\\d+)', trackData[j])[k])
                        bank.write(struct.pack('<d', fPlayAt))
                        fBeginTrimOffset = float(re.findall('fBeginTrimOffset\\: ([-]?\\d+)', trackData[j])[k])
                        bank.write(struct.pack('<d', fBeginTrimOffset))
                        fEndTrimOffset = float(re.findall('fEndTrimOffset\\: ([-]?\\d+)', trackData[j])[k])
                        bank.write(struct.pack('<d', fEndTrimOffset))
                        fSrcDuration = float(re.findall('fSrcDuration\\: ([-]?\\d+)', trackData[j])[k])
                        bank.write(struct.pack('<d', fSrcDuration))
                        bank.seek(4,1)
                    numAutos = int.from_bytes(bank.read(4), "little")
                    if numAutos > 8:
                        continue
                    if numAutos > 0: print(numAutos)
                    for autoCount in range(numAutos):
                        autoClip = int.from_bytes(bank.read(4), "little")
                        bank.seek(4,1)
                        numAutoSteps = int.from_bytes(bank.read(4), "little")
                        for n in range(numAutoSteps):
                            [fTimeIn] = struct.unpack('f',bank.read(4))
                            [fValIn] = struct.unpack('f',bank.read(4))
                            fCurveType = int.from_bytes(bank.read(4),"little")

                            if ('Automation ' + str(autoCount) + ' Point ' + str(n) + ' Time') in trackData[j]:
                                fTimeOut = float(re.findall('Automation ' + str(autoCount) + ' Point ' + str(n) + ' Time\\: ([-]?\\d+[.]?\\d*)', trackData[j])[autoClip])
                                if fTimeIn != fTimeOut:
                                    bank.seek(-12,1)
                                    bank.write(struct.pack('<f',fTimeOut))
                                    bank.seek(8,1)
                                    print("Reset time of automation " + str(autoCount) + " + " + str(n) + " from " + str(fTimeIn) + " to " + str(fTimeOut))

                            if ('Automation ' + str(autoCount) + ' Point ' + str(n) + ' Value') in trackData[j]:
                                fValOut = float(re.findall('Automation ' + str(autoCount) + ' Point ' + str(n) + ' Value\\: ([-]?\\d+[.]?\\d*)', trackData[j])[autoClip])
                                if fValIn != fValOut:
                                    bank.seek(-8,1)
                                    bank.write(struct.pack('<f',fValOut))
                                    bank.seek(4,1)
                                    print("Reset value of automation " + str(autoCount) + " + " + str(n) + " from " + str(fValIn) + " to " + str(fValOut))

        elif HIRCItem == 13:
            HIRCItemData = bank.read(HIRCItemSize)
            IDC = int.from_bytes(HIRCItemData[:4], "little")
            if IDC not in MusicRanSeqList:
                bank.seek(CurrOff + HIRCItemSize + 5)
                continue
            fVolume = 0
            bank.seek(CurrOff + 22)
            j = MusicRanSeqList.index(IDC)
            propCheck = int.from_bytes(bank.read(1), "little")
            if propCheck > 0:
                volumeProp = 0
                for iteration in range(propCheck):
                    propCheck2 = int.from_bytes(bank.read(1), "little")
                    if propCheck2 == 0:
                        volumeProp = iteration
                        bank.seek(CurrOff + 23 + propCheck)
                        break
                for iter2 in range(volumeProp):
                    bank.seek(4,1)
                fVolumeFinds = re.findall('\\* \\[Volume\\]:\\s+([-]?\\d+[.]?\\d*)',MusicRanSeqData[j])
                if len(fVolumeFinds) > 0:
                    fVolume = float(fVolumeFinds[0])
                    outputOff = struct.unpack('f',bank.read(4))
                    if fVolume != outputOff:
                        bank.seek(-4,1)
                        bank.write(struct.pack('<f', float(fVolume)))
                        print("Music Playlist " + str(IDC) + " attenuated!")
            
        else:
            bank.seek(HIRCItemSize,1)                    
        bank.seek(CurrOff + HIRCItemSize + 5)
        
    bank.close()
    print("Done!")


if len(sys.argv) > 1:
    run(sys.argv[1])
else:
    print("Nothing done.")
    print("Specify a WWise soundbank without the extension.")
    print("An unmodifed copy with extension \"soundbank_vanilla\" should already exist!")
