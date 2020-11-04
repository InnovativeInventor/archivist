#!/usr/bin/env python3

import sys
import json
import requests
import logger
import time
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root(url: str):
    r = fetch_response(url)
    if not r.get("archived_snapshots").get("closest"):
        logger.Logger.log_info("Not in WBM")
        with open("items.txt", "a") as f:
            f.write("!ao " + url + "\n")
        return {"Success": True}
    else:
        logger.Logger.log_info("In WBM")
        return {"Success": False}
    return {"Success": False}

def fetch_response(url: str, delay: int = 3):
    wbm_url = "http://archive.org/wayback/available?url={url}"
    try:
        r = requests.get(wbm_url.format(url=url).rstrip()).json()
    except json.decoder.JSONDecodeError:
        logger.Logger.log_info("Rate limiting?")
        time.sleep(delay)
        return fetch_response(url, delay+3)
    return r

if __name__ == "__main__":
    counter = 0
    for count, line in enumerate(sys.stdin):
        url = line.rstrip()
        r = fetch_response(url)
        if not r.get("archived_snapshots").get("closest"):
            counter += 1
            logger.Logger.log_info("Not in WBM, counter is at " + str(counter))
            with open("items.txt", "a") as f:
                f.write("!ao " + url + "\n")
        else:
            logger.Logger.log_info("In WBM")

