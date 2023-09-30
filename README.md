# RACRA-WWise

Sound extraction scripts for Ratchet and Clan: Rift apart for PC

## Requirements

- Python 3
- [Wwiser]
- [vgmstream]
- [FFmpeg]

VGMStream and FFMpeg need to be installed in the included folders in this repository, or, if you're a Mac or Linux user, in /usr/local/bin. WWiser and its wwnames.db3 dependency need to be in the root folder of this repository.

[Wwiser]:	https://github.com/vgmstream/vgmstream
[vgmstream]:	https://github.com/bnnm/wwiser
[FFmpeg]:	https://github.com/FFmpeg/FFmpeg

## Usage

Simply run "python3 runme.py" in a commandline tool.

The scripts will ask for a language suffix (leave blank if you want SFX and music. Only English and Brazilian Portuguese are currently supported), as well as a keyword or phrase to filter by if desired (recommended since the full archives are large and this will take time to extract entirely). The console will start by outputting all of the banks within the soundbank files if it helps you determine the workable filters.