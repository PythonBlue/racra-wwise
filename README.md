# RACRA-WWise

Sound modding scripts for Ratchet and Clank: Rift apart for PC

## Requirements

- Python 3
- [Wwiser]
- [Modding Tool](https://github.com/Tkachov/Overstrike/tree/main/ModdingTool)

WWiser and its wwnames.db3 dependency need to be in the root folder of this repository.

[Wwiser]:	https://github.com/bnnm/wwiser

## Usage

1. Copy or move the desired "soundbank" and "wem" files (in the "d" subdirectory of the game) and "toc" into the root folder.

> Note that the SFX and music spans across multiple wem files: "wem_0", "wem_00", and "wem_1".

2. Simply run "python3 runme.py" in a commandline tool.

The scripts will ask for a language suffix (leave blank if you want SFX and music), as well as a keyword or phrase to filter by if desired. The console will start by outputting all of the banks within the soundbank files if it helps you determine the workable filters.

For files that are embedded in the wem files, the resulting filenames will correspond to if they were extracted using the included "wwiseriff.bms" quickbms script.

The following languages for dialog are supported:
- English (US)
- French
- German
- Italian
- Japanese
- Polish
- Portuguese (Brazilian)
- Russian
- Spanish
- Spanish (Latin America)

The remaining languages may be added later.

## Sound Replacement

The included "sound_replace" script also depends on modifying the txtp files generated using the extraction tools. To use, run the script from the commandline, with an argument specifying the basename of the soundbank, which should be extracted using the [Modding Tool hosted here]{https://github.com/Tkachov/Overstrike/tree/main/ModdingTool) and its extension renamed to "soundbank_vanilla".

### Additional TXTP Parameters ###
- **normalize** - for undoing realtime automation data and setting the volume to a constant gain between 0 and 1. Write in a CAkMusicTrack section in the generated TXTP files
- **fVolume** - another method of adjusting volume, if realtime automation is not used. Write in a CAkMusicSegment
- **fTempo** - the tempo of given music in a CAkMusicSegment. Likely only needed for transitioning from looping audio
- **fTimeNumerator** - the first value of the time signature in a CAkMusicSegment. Usually 4 in the game
- **fTimeDenominator** - the second value of the time signature in a CAkMusicSegment. Usually 4 in the game

**Not all sounds specify volume or automation! Use at your own risk!**

### Example Sound Replacement
- python sound_replace.py music

Finally, some audio is stored both in the wem archives and a small segment in the soundbank files for prefetch purposes, so no guarantees only modifying the wem archive will produce favorable results.

## Additional Notes About Extraction
While, needless to say, it is confirmed that sounds can be extracted, out of respect for Insomniac Games, the creator of this repo chose not to implement the code required to convert the wem files: this script only generates text files corresponding to them to assist with replacing sounds for modding purposes. A combination of quickbms and vgmstream (and ffmpeg, if a format other than WAV is desired) can already handle converting of Wwise audio anyway.

## Additional Notes About Sound Replacement (Modding Tool-specific)
If you hesitate to replace existing sounds completely, I've confirmed you can add new ones!

1. Create WEM files from your desired sounds using WWise, preferably the 2019 edition if you need the Opus codec used for the game (which goes for all of the dialog). Changing formats in the soundbank metadata may be implemented later
2. Confirm a sound ID that is unused in the game. Everything between 4294963200 and 4294967295 (the maximum possible ID) is guaranteed free game from what I've found, though there are more in many smaller ranges.
3. Rename the WEM file you wish to add to "E0000000" followed by a hexadecimal representation of the ID number you decided on, with no extension. For example, sound ID 4294963200 would become "E0000000FFFFF000"
4. Move the renamed file into your stage project's directory. Unless you're working with dialog, this will be in the "3" subdirectory of your project.
5. Use Modding Tool as usual (ignore the warning when creating a stage file about new assets not being implemented)

Happy modding!