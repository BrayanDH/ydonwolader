#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yt_dlp
import json

PROBLEMATIC_URL = "https://www.youtube.com/watch?v=uik8XAXwqBQ"

try:
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(PROBLEMATIC_URL, download=False)
        
        print("VIDEO TITLE:", info.get('title'))
        print("FORMATS AVAILABLE:", len(info.get('formats', [])))
        print("\nFormat IDs available:")
        for fmt in info.get('formats', [])[:10]:
            print(f"  - ID: {fmt.get('format_id')}, Format: {fmt.get('format')}")
            
except Exception as e:
    print("ERROR:", str(e))
