# <search.py> v1.1.2
# WCTA Browser search library
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

import requests as r
# Used to make http requests
import simplejson as j
# Used to parse returned json
import re
# Used to get filename for download
from bs4 import BeautifulSoup as bs
# Used to decode the html table returned by the site

__INDEXURL__ = "https://ct.wiimm.de/index" # Search page
__APIURL__ = "https://ct.wiimm.de/api/get-track-info?" # Undocumented API
__DOWNURL__ = "https://ct.wiimm.de/d/{id}" # Download page
__IMGURL__ = "https://ct.wiimm.de/img/start/{id}" # Image URL

# Set URLs for different tasks.

# getCookie() - Retrieves a fresh cookie from wiimm.de
def getCookie():
    try:
        req = r.get(__INDEXURL__)
        req.raise_for_status()
        return req.cookies["CT_WIIMM_DE_SESSION24"]
    
    # Makes a request to the index and then extracts cookie from reply.
    
    except r.exceptions.HTTPError:
        print("H!")
        return None
        
    except r.exceptions.ConnectionError:
        print("H!")
        return None
    
    # Catch errors.
    
# setSearchLayout() - Sets the correct search layout, saved server side based
# on cookie.
def setSearchLayout(cookie):
    header = {"Cookie": "CT_WIIMM_DE_SESSION24={}".format(cookie)}
    payload = {"ajax": "track1", "ai": "24684738,N-fPdNFv3QsN", "pc": "0", 
               "seq": "3", "j": "Pview", "view": "xname"}
    
    # Magic payload that sets the correct layout
    
    try:
        req = r.post(__INDEXURL__, headers=header, data=payload)
        req.raise_for_status()
        
        # performs an empty search.
        
    except r.exceptions.HTTPError:
        print("H!")
        return None
        
    except r.exceptions.ConnectionError:
        print("H!")
        return None
    
def doSearch(cookie, request, resNum):
    header = {"Cookie": "CT_WIIMM_DE_SESSION24={}".format(cookie)}
    payload = {"type": "0", "search": request, "upd": "+Search+"}
    
    html = r.post(__INDEXURL__, headers=header, data=payload).text
    htmlsoup = bs(html, "lxml")
    
    table = htmlsoup.find(id="p1-tbody")
    tracks = []
    for i in range(resNum):
        tracks.append(table.find(id="p1-{}-0".format(i)))
        
    return tracks
    
# getTrackInfo() - Gets track information using SHA1 or track ID.
def getTrackInfo(isSHA1, identifier, cookie):
    header = {"Cookie": "CT_WIIMM_DE_SESSION24={}".format(cookie)}
    
    if isSHA1:
        apikey = "sha1="
        
    else:
        apikey = "fileid="
        
    # Sets correct API request based on supplied info
    
    url = __APIURL__ + apikey + str(identifier)
    
    try:
        req = r.get(url, headers=header)
        req.raise_for_status()
    
    except r.exceptions.HTTPError:
        print("I!")
        exit(1)
        
    except r.exceptions.ConnectionError:
        print("H!")
        return None
    
    return j.loads(req.text)
    # Extract json from returned request.
    
def downloadTrack(trackID, cookie):
    header = {"Cookie": "CT_WIIMM_DE_SESSION24={}".format(cookie)}
    url = __DOWNURL__.format(id=trackID)
    
    try:
        req = r.get(url, headers=header, stream=True)
        # Stream for file request.
        req.raise_for_status()
    
    except r.exceptions.HTTPError:
        print("I!")
        exit(1)
        # In this case, you've probably exceeded the allowed
        # download limit in the last hour.
        # This is based on IP, not much you can do.
        
    except r.exceptions.ConnectionError:
        print("H!")
        return None
    
    try:
        cD = req.headers["Content-Disposition"]
        fn = re.match(r'attachment; filename="([^"]*)"', cD).group(1)
        # Stupid hack to get the right filename
        
    except KeyError:
        print("I!")
        exit(1)
        # ID doesn't exist
        
    with open(fn, 'wb') as f:
        for chunk in req.iter_content(chunk_size=64):
            f.write(chunk)
    # code direct from requests documentation lol

def downloadImage(trackID, cookie):
    header = {"Cookie": "CT_WIIMM_DE_SESSION24={}".format(cookie)}
    url = __IMGURL__.format(id=trackID)
    
    try:
        req = r.get(url, headers=header, stream=True)
        # Stream for file request.
        req.raise_for_status()
    
    except r.exceptions.HTTPError:
        print("I!")
        exit(1)
        # In this case, you've probably exceeded the allowed
        # download limit in the last hour.
        # This is based on IP, not much you can do.
        
    except r.exceptions.ConnectionError:
        print("H!")
        return None
    
    with open(str(trackID)+".png", "wb") as f:
        for chunk in req.iter_content(chunk_size=64):
            f.write(chunk)
