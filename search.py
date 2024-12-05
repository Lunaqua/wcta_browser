# <search.py> v0.0.1
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

__INDEXURL__ = "https://ct.wiimm.de/index"
__APIURL__ = "https://ct.wiimm.de/api/get-track-info?"
__DOWNURL__ = "https://ct.wiimm.de/d/{id}"

def getCookie():
    try:
        req = r.get(__INDEXURL__)
        req.raise_for_status()
        return req.cookies["CT_WIIMM_DE_SESSION24"]
    
    except r.exceptions.HTTPError:
        print("H!")
        return None
        
    except r.exceptions.ConnectionError:
        print("H!")
        return None
    
def setSearchLayout(cookie):
    header = {"Cookie": "CT_WIIMM_DE_SESSION24={}".format(cookie)}
    payload = {"ajax": "track1", "ai": "24684738,N-fPdNFv3QsN", "pc": "0", 
               "seq": "3", "j": "Pview", "view": "xname"}
    
    try:
        req = r.post(__INDEXURL__, headers=header, data=payload)
        req.raise_for_status()
        
    except r.exceptions.HTTPError:
        print("H!")
        return None
        
    except r.exceptions.ConnectionError:
        print("H!")
        return None
    
def getTrackInfo(isSHA1, identifier, cookie):
    header = {"Cookie": "CT_WIIMM_DE_SESSION24={}".format(cookie)}
    
    if isSHA1:
        apikey = "sha1="
        
    else:
        apikey = "fileid="
    
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
    
    json = j.loads(req.text)
    print(json["file_name"])
