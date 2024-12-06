#!/bin/python3
# <wcta_browser.py> v0.0.3
# WCTA Browser main script.
#
# The MIT License (MIT)
# 
# Copyright © 2024 Navi4205 <lunaqua@proton.me>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the “Software”), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# import loadspin as ls
# Used to display a fancy little loading animation
import search
# Search/Download library
import track
# Track class library
import argparse as ap
# ArgumentParser
import simplejson as j
# Used to manage settings.
import time
# Used to provide the time for checking cookie expiration
# from multiprocessing import Process
# Allows running loadspin in the background
from pathlib import Path
# For check settings existance, and other file operations

### TODO
#
# Add help descriptions
# Allow stdin for -i and -s, for piping ids
# Add proper info retreval/storage
# Add error info for max download limit
# Add cache for trackinfo
# Review code at this point
# Add GUI at some point

__VERSION__ = "0.0.3"
__SETTINGS__ = "settings.json"
__INDEXURL__ = "https://ct.wiimm.de/index"
# Define basic information


# arginit() - define command-line arguments.
def arginit():
    parser = ap.ArgumentParser(
        prog="./wcta_browser.py",
        description="WCTA Browser",
        epilog="This software is distributed under the MIT License (MIT).")
    
    # parser.add_argument("-I", "--interactive", 
    #                     action="store_true")
    
    parser.add_argument("-V", "--version",
                        action="store_true")
    
    parser.add_argument("-R", "--refresh-cookie",
                        action="store_true")
    
    inputGroup = parser.add_mutually_exclusive_group()
    inputGroup.add_argument("-i", "--id", type=int)
    inputGroup.add_argument("-s", "--sha1")
    # Ensure id and sha1 cannot be used at the same time;
    # Only want to get info about one or the other.
    
    parser.add_argument("-d", "--download", type=int)
    
    return parser.parse_args()
    # Return parse_args object, for easy access to arguments.

# getSettings() - get settings from file.
def getSettings():
    pJson = Path(__SETTINGS__)
    if not pJson.is_file():
        print("S!")
        exit(1)
        
    # Checks to see if file exists
    
    with open(__SETTINGS__, "r") as sFile:
        sJson = j.load(sFile)
        
    if not sJson["magic"] == "wcta":
        print("S!")
        exit(1)
        
    # Basic validity check
        
    if not sJson["ver"] == 1:
        print("S?")
        
    # Basic version check, ensures file contains all
    # required arguments.
        
    return sJson
    
# saveSettings() - Save settings to file
def saveSettings(json):
    with open(__SETTINGS__, "w") as sFile:
        j.dump(json, sFile)
        
def displayTrackInfo(trackJson):
    trk = track.newTrack(trackJson)
    print(trk)

def main():
    args = arginit()
    # Get command line arguments
    
    if args.version:
        print("WCTA Browser v{} ---".format(__VERSION__))
        print("This software is distributed under the MIT License (MIT).")
        exit(0)
        
    # Display version information and exit.
   
    # if args.interactive:
    #     print("WCTA Browser v{} ---".format(__VERSION__))
    #     print("This software is distributed under the MIT License (MIT).")
    #     p = Process(target=ls.load)
    #     p.start()
        
    sJson = getSettings()
    
    # Get settings from file
        
    if sJson["cookie"] == "" or sJson["expiry"] < time.time() or args.refresh_cookie:
        # Check if cookie exists, is out of date or user wants manual refresh.
        cookie = search.getCookie()
        if cookie is None:
            exit(1)
        # Get new cookie
        
        sJson["cookie"] = cookie
        sJson["expiry"] = time.time() + 2592000
        saveSettings(sJson)
        # Save to settings file
        
        search.setSearchLayout(sJson["cookie"])
        # Sets the search page layout.
    
    if args.id:
        trackJson = search.getTrackInfo(False, args.id, sJson["cookie"])
        displayTrackInfo(trackJson)
    
    if args.sha1:
        trackJson = search.getTrackInfo(True, args.sha1, sJson["cookie"])
        displayTrackInfo(trackJson)
        
    # Gets track info
    
    if args.download:
        search.downloadTrack(args.download, sJson["cookie"])

if __name__ == "__main__":
    main()
