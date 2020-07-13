#!/usr/bin/env python3

import sys
import json
import requests
import logger
import time

def fetch_response(url: str, delay: int = 3):
    wbm_url = "http://archive.org/wayback/available?url={url}"
    try:
        r = requests.get(wbm_url.format(url=url).rstrip()).json()
    except json.decoder.JSONDecodeError:
        logger.Logger.log_info("Rate limiting?")
        time.sleep(delay)
        return fetch_response(url, delay+3)
    return r

counter = 0
for count, line in enumerate(sys.stdin):
    url = line.rstrip()
    r = fetch_response(url)
    if not r.get("archived_snapshots").get("closest"):
        counter += 1
        logger.Logger.log_info("Not in WBM, counter is at " + str(counter))
        with open("items.txt", "a") as f:
            f.write(url + "\n")
    else:
        logger.Logger.log_info("In WBM")


