import base64
import glob
import datetime
import os
import secrets
from multiprocessing import Pool

import requests
import snscrape.modules
import validators

import logger

DEDUP = False
DEDUP_LOC = "http://100.73.113.91:3000/"
proxies = []

def snscrape_commands():
    with open("snscrape.txt") as f:
        for each_line in f:
            yield each_line.rstrip()

def check_filter(url: str, sleep = 10) -> str:
    if DEDUP:
        try:
            return requests.get(DEDUP_LOC + base64.urlsafe_b64encode(str(url).rstrip().encode()).decode()).text
        except requests.exceptions.ConnectionError:
            logger.Logger.log_info(str(e))
            logger.Logger.log_info("Error, delaying")
            time.sleep(sleep)
            return check_filter(url, sleep+30)
    else:
        return True


def main():
    if DEDUP:
        assert not check_filter("test")
        test_str = secrets.token_hex(8)
        assert check_filter(test_str) == test_str
        assert not check_filter(test_str) == test_str
    # p = subprocess.Popen(["go", "run", "deduplicate.go"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    # child = pexpect.spawn('go run deduplicate.go', timeout=6000)
    # child.delaybeforesend = None

    # for count, line in enumerate(sys.stdin):
    logger.Logger.log_info("Reading from snscrape.txt")
    commands = list(snscrape_commands())
    list(map(writejob, commands))
    # with Pool(4) as p:
    #     p.map(writejob, commands)

def writejob(line):
    logger.Logger.log_info(line)
    filename = "jobs/" + datetime.datetime.today().strftime('%Y%m') + "/"
    directory = filename
    line = line.rstrip().split() 
    if not glob.glob(directory + "*" + line[2] + "*"):
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

        elif line[1] == "twitter-hashtag":
            filename += "twitter-hashtag-{arg}"
            scraper = snscrape.modules.twitter.TwitterHashtagScraper(line[2])

        else:
            raise ValueError(" ".join(line))

        filename = filename.format(arg=line[2])
        
        filename += "-" + datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        jsonname=filename + ".jsonl"
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

        try:
            with open(jsonname, "w") as j:
                j.write(scraper.entity.json() + "\n")
                with open(filename, "w") as f:
                    items = list(scraper.get_items())
                    for count, each_item in enumerate(items):
                        if DEDUP:
                            url = check_filter(str(each_item))
                        else:
                            url = str(each_item).rstrip()

                        j.write(each_item.json() + "\n")

                        if url and validators.url(url):
                            # logger.Logger.log_info("At item " + str(count) + " " + url)
                            f.write(url + "\n")

            logger.Logger.log_info("Done with " + filename)
        except KeyError:
            with open("error.log", "a+") as e:
                e.write("KeyError with " + filename + "\n")
            logger.Logger.log_info("KeyError with " + filename)
        except KeyboardInterrupt:
            print(line)
            raise KeyboardInterrupt
    else:
        logger.Logger.log_info(f"Skipped {line}")

    logger.Logger.log_info("Done")

if __name__ == "__main__":
    main()
