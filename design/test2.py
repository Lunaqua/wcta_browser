#!/bin/python

import requests as r
# Used to download the information page for the track
import simplejson as j
# Used to decode the json to python structures
from dataclasses import dataclass as dc
# Used to create a class for holding track info

@dc
class Track:
    id: int
    title: str
    type: str
    tclass: str
    name: str
    ver: str
    authors: list[str]
    familynum: int
    clannum: int
    sha1: str
    recslot: int
    musicslot: float
    prefix: str = None

# Defines the most important information for a track

def getTrack(json):
    return Track(json["file_id"],
                 json["file_name"],
                 "Arena" if json["is_arena"] else "Track", 
                 json["class"], 
                 json["split_name"]["name"],
                 json["split_name"]["version"],
                 json["split_name"]["authors"],
                 json["family"], 
                 json["clan"],
                 json["sha1"], 
                 json["slot"],
                 json["music_id"],
                 json["split_name"]["prefix"])

url = "https://ct.wiimm.de/api/get-track-info?fileid={}"
# Undocumented API endpoint
header = {"Cookie": "CT_WIIMM_DE_SESSION24=3645888-Zv7L5ABJLAJaHtLLQAPJyWBU"}
# required cookie, should be periodcally refreshed.

ref = int(input("Enter a track id: "))

try:
    req = r.get(url.format(ref), headers=header)
    req.raise_for_status()
    
except r.exceptions.HTTPError:
    print("Invalid ID")
    exit(1)

json = j.loads(req.text)
newTrack = getTrack(json)

print("\033[34;1m{}\033[0m\n".format(newTrack.title))
print("\033[1mID\033[0m - {:>18}".format(newTrack.id), end="")
print("\033[1m Family\033[0m - {:>14}".format(newTrack.familynum))
print("\033[1mName\033[0m - {:>40}".format(newTrack.name))
print("\033[1mAuthors\033[0m - {:>37}".format(newTrack.authors))
print("\033[1mVersion\033[0m - {:>37}".format(newTrack.ver))
print("\033[1mSHA1\033[0m - {:>40}".format(newTrack.sha1))
