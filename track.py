# <track.py> v1.2.1
# WCTA Browser track class/library
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

from dataclasses import dataclass as dc
# Used to create a class for holding track info
import time
# Converts unix time to actual time

@dc
class Track:
    id: int             # Track ID
    catID: int          # Category ID 
                        # https://ct.wiimm.de/stat/keywords#category
    catInfo: str        # Category Info
    title: str          # Full track filename
    type: str           # Either Track or Arena
    multi: bool         # Multiplayer?
    tClass: str         # https://ct.wiimm.de/stat/keywords#class
    name: str           # Track name
    combName: str       # Combined name with prefix
    ver: str            # Track Version
    authors: list[str]  # List of Authors
    attrib: list[str]   # List of Attributes
    familyNum: int      # Family ID
    clanNum: int        # Clan ID
    sha1: str           # SHA 1 Hash
    recSlot: int        # Recommended Slot
    musicSlot: float    # Recommended Music Slot (according to wiimm :p)
    badSlot: list[str]  # Slots that don't work
    editors: list[str]  # List of Editors
    date: str           # Date and Time of creation
    rawdate: int        # Date in unix time
    lapCounters: int    # Number of lap counters
    laps: int           # Number of laps
    speed: int          # Speed Modifier
    wikiPageID: int     # Custom Track Wiiki Page ID
    prefix: str = None  # Primary Prefix (if it exists)
    secPrefix: str = None # Secondary Prefix (if it exists)
    multiID: int = None # If multiplayer, ID
    extra: str = None   # extra info?
    

def newTrack(json):
    if json["split_name"]["prefix2"]:
        combName = json["split_name"]["prefix1"] + " " + json["split_name"]["prefix2"] + " " + json["split_name"]["name"]
    elif json["split_name"]["prefix1"]:
        combName = json["split_name"]["prefix1"] + " " + json["split_name"]["name"]
    else:
        combName = json["split_name"]["name"]
    
    return Track(json["file_id"],
                 json["category"]["id"],
                 json["category"]["info"],
                 json["file_name"],
                 "Arena" if json["is_arena"] else "Track",
                 json["is_d"],
                 json["class"], 
                 json["split_name"]["name"],
                 combName,
                 json["split_name"]["version"],
                 json["split_name"]["authors"].split(","),
                 json["split_name"]["attributes"].split(","),
                 json["family"], 
                 json["clan"],
                 json["sha1"], 
                 json["slot"],
                 json["music_id"],
                 json["slot_info"].split(","),
                 json["split_name"]["editors"].split(",") if json["split_name"]["editors"] else None,
                 time.ctime(json["szs_time"]),
                 json["szs_time"],
                 json["ckpt_lap_counters"],
                 json["stgi_laps"],
                 json["stgi_speed"],
                 json["ctwiki_pageid"],
                 json["split_name"]["prefix1"],
                 json["split_name"]["prefix2"],
                 json["d_id"],
                 json["split_name"]["extra"])
                 
