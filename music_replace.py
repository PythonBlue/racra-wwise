import os, re, struct

bank = open("banks" + os.path.sep + "soundbank_323.bnk", "rb+")
bank.seek(0,2)
bankSize = bank.tell()

tracks = []
trackData = []
segments = []
segmentData = []
for file in sorted(os.listdir("banks" + os.path.sep + "txtp")):
    if file.endswith(".txtp"):
        txtp = open("banks" + os.path.sep + "txtp" + os.path.sep + file, "r")
        txtpRead = txtp.read()
        txtp.close()
        listFind = re.findall(' wem.+', txtpRead)
        segmentFind = re.findall('CAkMusicSegment[\[]\d+[\]]\s+\d+', txtpRead)
        if len(segmentFind) <= 0:
            continue
        segmentOff = []
        for count in range(len(segmentFind)):
            segmentOff.append(txtpRead.find(segmentFind[count]))
        for count in range(len(segmentFind)):
            resultLength = txtpRead[segmentOff[count]:]
            resultLength = resultLength.split(" ")[1].split("\n#\n")[0]
            #print(resultLength)
            segments.append(resultLength)
            segmentData.append(txtpRead[segmentOff[count]:])
                    
        trackFind = re.findall('CAkMusicTrack[\[]\d+[\]]\s+\d+', txtpRead)
        if len(trackFind) <= 0:
            continue
        trackOff = []
        for count in range(len(trackFind)):
            trackOff.append(txtpRead.find(trackFind[count]))
        for count in range(len(trackFind)):
            resultLength = txtpRead[trackOff[count]:]
            resultLength = resultLength.split(" ")[1]
            if resultLength.count('CAkMusicTrack') > 1:
                resultLength = 'CAkMusicTrack' + resultLength.split('CAkMusicTrack')[1]
            if 'CAkMusicSegment' in resultLength:
                resultLength = resultLength.split('CAkMusicSegment')[0]
            if 'AkMusicRanSeqPlaylistItem' in resultLength:
                resultLength = resultLength.split('AkMusicRanSeqPlaylistItem')[0]
            #print(resultLength)
            tracks.append(resultLength)
            trackData.append(txtpRead[trackOff[count]:])

        

bank.seek(0)
HIRCStart = 0
while bank.tell() < bankSize - 1048576:
    bankStart = bank.tell()
    bankRead = bank.read(2097152)
    if b'HIRC' in bankRead:
        HIRCStart = bankStart + bankRead.find(b'HIRC')
bank.seek(HIRCStart + 4)
HIRCSize = int.from_bytes(bank.read(4), "little")
HIRCCount = int.from_bytes(bank.read(4), "little")
for i in range(HIRCCount - 32):
    CurrOff = bank.tell()
    HIRCItem = int.from_bytes(bank.read(1), "little")
    HIRCItemSize = int.from_bytes(bank.read(4), "little")
    if HIRCItem != 10 and HIRCItem != 11:
        bank.seek(HIRCItemSize,1)
    if HIRCItem == 10:
        HIRCItemData = bank.read(HIRCItemSize)
        for j in range(len(segments)):
            segCheck = int(segments[j].split("\n")[0]).to_bytes(4, "little")
            #print(segCheck)
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
                    fVolumeFinds = re.findall('Volume:\s+([-]?\d+[.]?\d*)',segmentData[j])
                    if len(fVolumeFinds) > 0:
                        fVolume = float(fVolumeFinds[0])
                        bank.write(struct.pack('<f', float(fVolume)))
                        
                bank.seek(CurrOff + 5)
                fDuration = float(segmentData[j][segmentData[j].find('fDuration: ') + 11:].split('\n')[0])
                fEndMark = re.findall('AkMusicMarkerWwise:\s+(\d+[.]?\d*)',segmentData[j])
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
    bank.seek(CurrOff + HIRCItemSize + 5)

bank.close()
print("Done!")
