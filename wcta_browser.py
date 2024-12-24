#!/bin/python3
# <wcta_browser.py> v1.0.3
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
# Allow stdin for -i and -s, for piping id/sha1
# Add options to print different info for search
# Allow search for tracks/arenas only
# Add error info for max download limit
# Add sixel output for images
# Add cache for trackinfo
# Review code at this point
# Download to stdout rather than file
#
# Add distribution support at some point
# Add support for SZS Library
# Add GUI at some point
# Add translation support at some point

__VERSION__ = "1.0.3"
__SETTINGS__ = "settings.json"
__INDEXURL__ = "https://ct.wiimm.de/index"
# Define basic information


# arginit() - define command-line arguments.
def arginit():
    parser = ap.ArgumentParser(
        prog="./wcta_browser.py",
        description="WCTA Browser v{}".format(__VERSION__),
        epilog="This software is distributed under the MIT License (MIT).")
    
    # parser.add_argument("-I", "--interactive", 
    #                     action="store_true")
    
    parser.add_argument("-V", "--version",
                        action="store_true",
                        help="display version information")
    
    parser.add_argument("-R", "--refresh-cookie",
                        action="store_true",
                        help="manually refresh cookie")
    
    parser.add_argument("-C", "--colour",
                        action="store_true",
                        help="enable colour output")
    
    infoGroup = parser.add_argument_group("track info")
    inputGroup = infoGroup.add_mutually_exclusive_group()
    inputGroup.add_argument("-i", "--id", type=int, help="lookup track id")
    inputGroup.add_argument("-S", "--sha1", help="lookup track sha1")
    
    # Ensure id and sha1 cannot be used at the same time;
    # Only want to get info about one or the other.
    
    parser.add_argument("-d", "--download", metavar="ID", type=int, 
                        help="download specified id")
    infoGroup.add_argument("-p", "--print", "--display", metavar="ITEM,ITEM",
                        help="display track information")
    infoGroup.add_argument("-a", "--all",
                           action="store_true",
                           help="display all information (ignores -p)")
    infoGroup.add_argument("-I", "--img", action="store_true",
                            help="download track image")
    
    searchGroup = parser.add_argument_group("search info")
    searchGroup.add_argument("-s", "--search",
                             help="search for a track")
    searchGroup.add_argument("-n", "--num", "--results", type=int,
                             help="print a specific number of results.")
    
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
        
    if not sJson["ver"] == 2:
        print("S?")
        
    # Basic version check, ensures file contains all
    # required arguments.
        
    return sJson
    
# saveSettings() - Save settings to file
def saveSettings(json):
    with open(__SETTINGS__, "w") as sFile:
        j.dump(json, sFile)
        
# displayTrackInfo() - Display track information
def displayTrackInfo(trackJson, css, colour, printAll):
    trk = track.newTrack(trackJson)
    # Convert json file into class containing values
    
    if css:
        csl = css.split(",")
        # Split user input into keys
        
    # Check for print all option, and if enabled display all
    elif printAll:
        csl = trk.__dict__
        
    else:
        csl = []
        
    # Detects whether to use colour
    if colour:
        for i in csl:
            try:
                match i:
                    case "combName" if getattr(trk, "secPrefix"):
                        txt = getattr(trk,i).split(" ",maxsplit=2)
                        print("\033[1m{} {}\033[0m {}".format(txt[0], txt[1], txt[2]))
                    
                    case "combName" if getattr(trk, "prefix"):
                        txt = getattr(trk,i).split(" ",maxsplit=1)
                        print("\033[1m{}\033[0m {}".format(txt[0], txt[1]))
                    
                    case "title":
                        print("\033[34;1m{}\033[0m".format(getattr(trk, i)))
                    
                    case _:
                        print(getattr(trk, i))
                
            except AttributeError:
                print("P?")
                # Ensures program does not crash on unknown attrib
    
    else:
        # Simple print for without colour
        for i in csl:
            try:
                print(getattr(trk, i))
                
            except AttributeError:
                print("P?")

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
        
    if args.search:
        resNum = args.num if args.num else 10
        tracks = search.doSearch(sJson["cookie"], args.search, resNum)
        for i in tracks:
            if i is None:
                continue
            
            info = i.find_all("td")
            print("{}: ".format(info[2].string), end="")
            print(info[9].contents[0])
    
    if args.id:
        trackJson = search.getTrackInfo(False, args.id, sJson["cookie"])
        # Gets json with track info
        colour = True if args.colour or sJson["colour"] else False
        # Checks for colour being set either way
        displayTrackInfo(trackJson, args.print, colour, args.all)
        # Displays track info 
        if args.img:
            search.downloadImage(args.id, sJson["cookie"])
    
    if args.sha1:
        trackJson = search.getTrackInfo(True, args.sha1, sJson["cookie"])
        colour = True if args.colour or sJson["colour"] else False
        displayTrackInfo(trackJson, args.print, colour, args.all)
        
    # Gets track info
    
    if args.download:
        search.downloadTrack(args.download, sJson["cookie"])

if __name__ == "__main__":
    main()
