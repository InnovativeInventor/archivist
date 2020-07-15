import subprocess
import base64
import secrets
import datetime
import time
import validators
import snscrape.modules
import pexpect
import os
import sys
import logger
import requests

DEDUP_LOC = "http://127.0.0.1:3000/"

def snscrape_commands():
    with open("snscrape.txt") as f:
        for each_line in f:
            yield each_line.rstrip()

def check_filter(url: str) -> str:
    return requests.get(DEDUP_LOC + base64.urlsafe_b64encode(str(url).rstrip().encode()).decode()).text

def main():
    # p = subprocess.Popen(["go", "run", "deduplicate.go"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    # child = pexpect.spawn('go run deduplicate.go', timeout=6000)
    # child.delaybeforesend = None

    # for count, line in enumerate(sys.stdin):
    logger.Logger.log_info("Reading from snscrape.txt")
    for count, line in enumerate(snscrape_commands()):
        if line := line.rstrip().split():
            filename = "jobs/" + datetime.datetime.today().strftime('%Y%m%d') + "/"
            directory = filename

            if line[1] == "twitter-user":
                filename += "twitter-@{arg}"
                scraper = snscrape.modules.twitter.TwitterUserScraper(username=line[2])

            elif line[1] == "facebook-user":
                filename += "facebook-@{arg}"
                scraper = snscrape.modules.facebook.FacebookUserScraper(line[2])
                
            elif line[1] == "facebook-group":
                filename += "facebook-group-{arg}"
                scraper = snscrape.modules.facebook.FacebookGroupScraper(line[2])

            elif line[1] == "twitter-list":
                filename += "twitter-list-{arg}"
                scraper = snscrape.modules.twitter.TwitterListPostsScraper(line[2])

            else:
                raise ValueError(" ".join(line))

            filename = filename.format(arg=line[2])
            filename += "-" + datetime.datetime.today().strftime('%Y%m%d')
            filename += ".txt"

            logger.Logger.log_info("Job " + filename)

            # snscrape = subprocess.run(line, capture_output=True, text=True)
            # snscrape = subprocess.Popen(line, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # snscrape = pexpect.spawn(" ".join(line))

            # child.expect('Ok', timeout=600)
            # child.expect('Ready', timeout=600)
            # response = p.stderr.readline().decode()
            # if not "Ok" in response:
                # logger.Logger.log_info(response)
                # break

            # response = p.stderr.readline().decode()
            # if not "Ready" in response:
                # logger.Logger.log_info(response)
                # break
            # time.sleep(1)

            if not os.path.exists(directory):
                os.makedirs(directory)

            assert not check_filter("test")
            test_str = secrets.token_hex(8)
            assert check_filter(test_str) == test_str
            with open(filename, "w") as f:
                for count, each_item in enumerate(scraper.get_items()):
                    url = check_filter(str(each_item))

                    if url and validators.url(url):
                        logger.Logger.log_info("At item " + str(count) + " " + url)
                        f.write(url)

            logger.Logger.log_info("Done with " + filename)


    logger.Logger.log_info("Done")

if __name__ == "__main__":
    main()
