import glob
import tqdm
import redis
import os

DIR = os.getenv("DIR")
files = glob.glob(DIR + "*")
r = redis.Redis(host='localhost', port=6379, db=0)

for each_file in tqdm.tqdm(files):
    with open(each_file) as f:
        for each_line in f:
            r.set(each_line.split("/")[-1].rstrip(), 1)
