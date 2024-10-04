#!/bin/python

import requests as r
# Used to download the information page for the track
from bs4 import BeautifulSoup as bs
# Used to decode the html table returned by the site
import simplejson as j
# Used to extract the html body from the json returned
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
#     familynum: int
    sha1: str
#     recslot: float
#     musicslot: float
#     dist: list[str]
    prefix: str = None
#     clannum: list[int, int] = None


# Defines the most important information for a track

def findValue(soup, searchStr:str):
    return soup.find(string=searchStr).find_parent("td").next_sibling

def getTrack(gISoup):
    tciL = str(findValue(gISoup, "Type, Class and Id:").string).split(" / ")
    try:
        pf = str(findValue(gISoup, "Console or prefix:").b.string)
    except AttributeError:
        pf = None
    
    tnv = findValue(gISoup, "Track name and version:")
    tn = tnv.b.string
    ver = str(tn.next_element.string)
    auL = str(findValue(gISoup, "Created by:").string).split(", ")
    sha = str(findValue(gISoup, "SHA1 checksum:").tt.string)
    
    return Track(id=int(tciL[2]), title=str(gISoup.tr.th.string), type=tciL[0], tclass=tciL[1], name=str(tn), ver=ver, prefix=pf, authors=auL, sha1=sha)

url = "https://ct.wiimm.de/ajax/get-info"
# get-info is a php script.
# used over index.php?ajax=ctt, as get-info contains more information.
# also used over i/[id], as parsing get-info is easier.
header = {"Content-Type": "application/x-www-form-urlencoded", 
          "Cookie": "CT_WIIMM_DE_SESSION24=3645888-Zv7L5ABJLAJaHtLLQAPJyWBU"}
# required cookie, should be periodically refreshed.

ref = int(input("Enter a track ref: "))
payload = {"f": ref}
# Sets up the required data for the script.

req = r.post(url, headers=header, data=payload)
# Sends the post request to the URL, and saves the response. should really
#   check the returned status.
htmlsoup = bs(j.loads(req.text)["modal"]["body"], "lxml").table
# Creates a new bs object from the returned decoded json, under modal, then
#   body keys, then the table element of the html

newTrack = getTrack(htmlsoup)

print("\033[34;1m{}\033[0m\n".format(newTrack.title))
print("\033[1mID\033[0m - {:>20}".format(newTrack.id))
print("\033[1mName\033[0m - {:>40}".format(newTrack.name))
print("\033[1mVersion\033[0m - {:>37}".format(newTrack.ver))
print("\033[1mSHA1\033[0m - {:>40}".format(newTrack.sha1))
