#!/usr/bin/env python3

import sys
import requests
import logger

counter = 0
for count, line in enumerate(sys.stdin):
    url = line.rstrip()
    wbm_url = "http://archive.org/wayback/available?url={url}"
    r = requests.get(wbm_url.format(url=url).rstrip()).json()
    if not r.get("archived_snapshots").get("closest"):
        counter += 1
        logger.Logger.log_info("Not in WBM, counter is at " + str(counter))
        with open("items.txt", "a") as f:
            f.write(url + "\n")
    else:
        logger.Logger.log_info("In WBM")


