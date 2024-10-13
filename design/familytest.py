#!/bin/python

import requests as r
# Used to download the sha1 checksums
import simplejson as j
# Used to browse the json
from pathlib import Path as p
# Used to find the .json file (if it exists)

sha1:str
url = "https://ct.wiimm.de/export/sha1ref/view+json/sha1-reference.json"
header = {"Cookie": "CT_WIIMM_DE_SESSION24=3645888-Zv7L5ABJLAJaHtLLQAPJyWBU"}

try:
    jsonF = p("sha1-reference.json")
    jsonPath = jsonF.resolve(strict=True)
except FileNotFoundError:
    req = r.get(url, headers=header)
    with open("sha1-reference.json", "w") as jsonF:
        jsonF.write(req.text)
        jsonF.close()

with open("sha1-reference.json", "r") as jsonF:
    json = j.load(jsonF)
    jsonF.close()
    
sha1 = input("Enter a valid track SHA1: ")
sEntry = json["data"][sha1]

print("\nTrack Found!")
print("\033[1mID\033[0m - {:>20}".format(sEntry[0]))
print("\033[1mFamily\033[0m - {:>16}".format(sEntry[1]))
print("\033[1mClan\033[0m - {:>18}".format(sEntry[2]))
print("\033[1mCFlags\033[0m - {:>16}".format(sEntry[3]))
