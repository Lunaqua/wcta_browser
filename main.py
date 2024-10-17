#!/bin/python3
# <main.py> - WCTA Browser main script.
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

import loadspin as ls
# Used to display a fancy little loading animation
import argparse as ap
# ArgumentParser
import requests as r
# Used to make http requests
import simplejson as j
# Used to manage settings.
import time
# Used to provide the time for checking cookie expiration

__VERSION__ = "0.0.1"
__SETTINGS__ = "settings.json"
__INDEXURL__ = "https://ct.wiimm.de/index"
# Define basic information

def arginit():
    parser = ap.ArgumentParser(
        prog="WCTA Browser")
    
    parser.add_argument("-I", "--interactive", 
                        action="store_true")
    
    return parser.parse_args()

def getSettings():
    with open(__SETTINGS__, "r") as sFile:
        return j.load(sFile)
    
def saveSettings(json):
    with open(__SETTINGS__, "w") as sFile:
        j.dump(json, sFile)
    
def getCookie():
    try:
        req = r.get(__INDEXURL__)
        req.raise_for_status()
        return req.cookies["CT_WIIMM_DE_SESSION24"]
    
    except r.exceptions.HTTPError:
        print("!")
        exit(1)
        
    except r.exceptions.ConnectionError:
        print("!")
        exit(1)

def main():
    args = arginit()
    if args.interactive:
        print("WCTA Browser v{} ---".format(__VERSION__))
        print("This software is distributed under the MIT License (MIT).")
        
    sJson = getSettings()
    if sJson["cookie"] == "" or sJson["expiry"] < time.time():
        cookie = getCookie()
        sJson["cookie"] = cookie
        sJson["expiry"] = time.time() + 2592000
        saveSettings(sJson)
    

if __name__ == "__main__":
    main()
