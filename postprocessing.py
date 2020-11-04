import glob
import shutil
import os
import json
import re
import datetime

"""
Ensures that the capitalization of the usernames are consistent and that the creation time (estimated) is in the filename.
Usage:
    python postprocessing.py
"""

good = re.compile(r"[0-9]*Z.txt")
bad = re.compile(r"[0-9]*.txt")

jobs = glob.glob("jobs/202011/*.txt")
path = "https://archive.max.fan/{job}"

for each_job in jobs:
    each_jsonl = each_job.replace(".txt", ".jsonl")
    if os.path.isfile(each_jsonl):
        estimated_creation_time = min(os.path.getctime(each_job), os.path.getmtime(each_job), os.path.getctime(each_job))
        estimated_creation_time_formatted = datetime.datetime.fromtimestamp(estimated_creation_time).strftime("%Y%m%dT%H%M%SZ")

        with open(each_jsonl) as f:
            try:
                tweet_obj = json.loads(next(f))
                # print(tweet_obj["username"])
                if tweet_obj["username"].rstrip() not in each_job:
                    rename = re.compile(re.escape(tweet_obj["username"]), re.IGNORECASE).sub(tweet_obj["username"], each_job)
                else:
                    rename = each_job

                if bad.search(each_job) and not good.search(each_job):
                    rename = bad.sub(estimated_creation_time_formatted + ".txt", rename)

                if rename.rstrip() != each_job.rstrip():
                    shutil.move(each_job, rename)
                print(path.format(job=rename))


            except StopIteration:
                continue




