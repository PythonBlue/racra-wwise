# RACRA-WWise

Sound extraction scripts for Ratchet and Clan: Rift apart for PC

## Requirements

- Python 3
- [Wwiser]

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

## Note
While, needless to say, it is confirmed that sounds can be extracted, out of respect for Insomniac Games, the creator of this repo chose not to implement the code required to convert the wem files: this script only generates text files corresponding to them to assist with replacing sounds for modding purposes. A combination of quickbms and vgmstream (and ffmpeg, if a format other than WAV is desired) can already handle converting of Wwise audio anyway.

The included "music_replace" script also depends on modifying the txtp files generated using the extraction tools and assumes they're in the same path. Required bank filename is "soundbank_323.bnk", which corresponds to if the bank of concern was extracted using the "wwisebnk.bms" quickbms script.

Finally, some audio is stored both in the bnk files and a small segment in the wem archives for prefetch purposes, so no guarantees only modifying the wem archive will produce favorable results.

Happy modding!