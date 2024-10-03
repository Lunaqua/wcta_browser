#!/bin/python

import requests as r

url = "https://ct.wiimm.de/ajax.php?ajax=ctt"
header = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": "CT_WIIMM_DE_SESSION24=3645888-Zv7L5ABJLAJaHtLLQAPJyWBU"}
payload = {"seq": "1", "j": "tooltip", "id": "ct-tooltip", "ref": "6841"}

req = r.post(url, headers=header, data=payload)
print(req.status_code)
print(req.content)

# url = "https://ct.wiimm.de/ajax.php?ajax=ctt&seq=1&j=tooltip&id=ct-tooltip&ref=6841"
# 
# req = r.get(url, headers=header)
# print(req.status_code)
# print(req.content)
