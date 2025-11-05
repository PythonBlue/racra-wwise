# RACRA-WWise

Sound modding scripts for Ratchet and Clank: Rift apart for PC

## Requirements

- Python 3
- [Wwiser]
- [Modding Tool](https://github.com/Tkachov/Overstrike/tree/main/ModdingTool)

WWiser and its wwnames.db3 dependency need to be in the root folder of this repository.

[Wwiser]:	https://github.com/bnnm/wwiser

## Usage (Extraction)

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

The included "sound_replace" script also depends on modifying the txtp files generated using the extraction tools. To use, run the script from the commandline, with an argument specifying the basename of the soundbank, which should be extracted using the [Modding Tool hosted here](https://github.com/Tkachov/Overstrike/tree/main/ModdingTool) and its extension renamed to "soundbank_vanilla".

As of September 21 2024, a custom build of wwiser.pyz is included that includes additional parameters for txtp creation, to further simplify sound analysis and modding for the game.

**Not all sounds specify volume or automation! Use those parameters at your own risk!**

Finally, some audio is stored both in the wem archives and a small segment in the soundbank files for prefetch purposes, so no guarantees only modifying the wem archive will produce favorable results.

## Usage (Editing and Replacement)

1. Create WEM files from your desired sounds using WWise, preferably the 2019 edition if you need the Opus codec used for the game (which goes for all of the dialog). Changing formats in the soundbank metadata may be implemented later (Updated September 21 2024 to have experimental format changing between Vorbis and Opus formats, the two known WEM formats in the game)

2. Load up the txtp file(s) with the wem ID you wish to edit in a text editor and go to the commented section that begins with "PATH". This is where the meat of the editing of the metadata will take place. Below are the values possible to change (asterisk items require the included build of wwiser to properly extract)

- [Volume]*
- fGridPeriod*
- fGridOffset*
- fTempo*
- uTimeSigNumBeatsBar*
- uTimeSigBeatValue*
- fDuration
- AkMusicMarkerWwise
- sourceID (make sure it lines up with the Source ID below it!)
- fPlayAt
- fBeginTrimOffset
- fEndTrimOffset
- fSrcDuration
- ulPluginID
- Automation # Point # Time*
- Automation # Point # Value*

3. If not already done, move all edited txtp files to the following path relative to the repo: "txtp\(name of the bank to edit)"

4. After changes are satisfactory, run the following command in a terminal set to the repo's directory:

- python sound_replace.py (name of the bank to edit)

- - Example: "python sound_replace.py music"

Alternatively, as of 4-6-2025, you can also replace music segments referenced by the gameplay without replacing the raw audio by running the "sound_replace" script with a ".lst" file (in actuality, a renamed text file) in the music folder containing lines in the following format:

- (Gamestate Name; can be obtained either in the txtp filenames or by looking through the MusicSwitchCntr information in them):(CAkMusicRanSeqCntr number (not the bracketed number)
- - Example: "OBJ_ZORDOOM_EVAC_PLAT_01_COMBAT:854756349"

5. Open Modding Tool and replace/add the new wem files, as well as the soundbanks containing anything edited with the txtp files.

6. Build, install, and test

## Additional Notes About Extraction
While, needless to say, it is confirmed that sounds can be extracted, out of respect for Insomniac Games, the creator of this repo chose not to implement the code required to convert the wem files: this script only generates text files corresponding to them to assist with replacing sounds for modding purposes. A combination of quickbms and vgmstream (and ffmpeg, if a format other than WAV is desired) can already handle converting of Wwise audio anyway.

## Additional Notes About Sound Replacement (Modding Tool-specific)
If you hesitate to replace existing sounds completely, I've confirmed you can add new ones!

1. Confirm a sound ID that is unused in the game. Everything between 4294963200 and 4294967295 (the maximum possible ID) is guaranteed free game from what I've found, though there are more in many smaller ranges.
2. Rename the WEM file you wish to add to "E0000000" followed by a hexadecimal representation of the ID number you decided on, with no extension. For example, sound ID 4294963200 would become "E0000000FFFFF000"
3. Move the renamed file into your stage project's directory. Unless you're working with dialog, this will be in the "3" subdirectory of your project.
4. Use Modding Tool as usual (ignore the warning when creating a stage file about new assets not being implemented)

Happy modding!