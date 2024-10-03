#!/bin/python

import requests as r
# Used to download the information page for the track
from bs4 import BeautifulSoup as bs
# Used to decode the html table returned by the site
import simplejson as j
# Used to extract the html body from the json returned

url = "https://ct.wiimm.de/ajax/get-info"
# get-info is a php script.
# used over index.php?ajax=ctt, as get-info contains more information.
# also used over i/[id], as parsing get-info is easier.
header = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": "CT_WIIMM_DE_SESSION24=3645888-Zv7L5ABJLAJaHtLLQAPJyWBU"}
# required cookie, should be periodically refreshed.

ref = int(input("Enter a track ref: "))
payload = {"f": ref}
# Sets up the required data for the script.

req = r.post(url, headers=header, data=payload)
# Sends the post request to the URL, and saves the response. should really
#   check the returned status.
htmlsoup = bs(j.loads(req.text)["modal"]["body"], "html.parser")
# Creates a new bs object from the returned decoded json, under modal, then
#   body keys.

print(htmlsoup.prettify())
# prints a new looking variation of the html.
