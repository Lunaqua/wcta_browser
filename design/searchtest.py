#!/bin/python

import requests as r
# Used to download the information page for the track
from bs4 import BeautifulSoup as bs
# Used to decode the html table returned by the site

url = "https://ct.wiimm.de/index"
header = {"Cookie": "CT_WIIMM_DE_SESSION24=3645888-Zv7L5ABJLAJaHtLLQAPJyWBU"}
payload = {"ajax": "track1", "ai": "24684738,N-fPdNFv3QsN", "pc": "0", "seq": "3", "j": "Pview", "view": "xname"}

req = r.post(url, headers=header, data=payload)
query = input("Enter a search query: ")
payload = {"type": "0", "search": query, "upd": "+Search+"}

html = r.post(url, headers=header, data=payload).text
htmlsoup = bs(html, "lxml")

table = htmlsoup.find(id="p1-tbody")
tracks = []
for i in range(10):
    tracks.append(table.find(id="p1-{}-0".format(i)))

for i in tracks:
    if i is None:
        continue
    info = i.find_all("td")
    print("{}: ".format(info[2].string), end="")
    print(info[9].contents[0])
