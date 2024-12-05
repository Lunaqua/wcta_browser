#!/bin/python3
# <main.py> v0.0.1
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
# Comment existing code
# Comment code in search
# Allow stdin for -i and -s, for piping ids.
# Add proper info retreval/storage
# Add cache for trackinfo
# Find a better way of using loadspin/interactive mode.

__VERSION__ = "0.0.1"
__SETTINGS__ = "settings.json"
__INDEXURL__ = "https://ct.wiimm.de/index"
# Define basic information

def arginit():
    parser = ap.ArgumentParser(
        prog="./main.py",
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
    
    return parser.parse_args()

def getSettings():
    pJson = Path(__SETTINGS__)
    if not pJson.is_file():
        print("S!")
        exit(1)
    
    with open(__SETTINGS__, "r") as sFile:
        sJson = j.load(sFile)
        
    if not sJson["magic"] == "wcta":
        print("S!")
        exit(1)
        
    if not sJson["ver"] == 1:
        print("S?")
        
    return sJson
    
def saveSettings(json):
    with open(__SETTINGS__, "w") as sFile:
        j.dump(json, sFile)

def main():
    args = arginit()
    
    if args.version:
        print("WCTA Browser v{} ---".format(__VERSION__))
        print("This software is distributed under the MIT License (MIT).")
        exit(0)
   
    # if args.interactive:
    #     print("WCTA Browser v{} ---".format(__VERSION__))
    #     print("This software is distributed under the MIT License (MIT).")
    #     p = Process(target=ls.load)
    #     p.start()
        
    sJson = getSettings()
        
    if sJson["cookie"] == "" or sJson["expiry"] < time.time() or args.refresh_cookie:
        cookie = search.getCookie()
        if cookie is None:
            exit(1)
        
        sJson["cookie"] = cookie
        sJson["expiry"] = time.time() + 2592000
        saveSettings(sJson)
        
        search.setSearchLayout(sJson["cookie"])
    
    if args.id:
        search.getTrackInfo(False, args.id, sJson["cookie"])
    
    if args.sha1:
        search.getTrackInfo(True, args.sha1, sJson["cookie"])

if __name__ == "__main__":
    main()
