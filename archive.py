import base64
import secrets
import datetime
import validators
import snscrape.modules
import os
import logger
import requests
from multiprocessing import Pool

DEDUP_LOC = "http://100.73.113.91:3000/"
proxies = []

def snscrape_commands():
    with open("snscrape.txt") as f:
        for each_line in f:
            yield each_line.rstrip()

def check_filter(url: str, sleep = 10) -> str:
    try:
        return requests.get(DEDUP_LOC + base64.urlsafe_b64encode(str(url).rstrip().encode()).decode()).text
    except requests.exceptions.ConnectionError:
        logger.Logger.log_info(str(e))
        logger.Logger.log_info("Error, delaying")
        time.sleep(sleep)
        return check_filter(url, sleep+30)


def main():
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
    with Pool(4) as p:
        p.map(writejob, commands)

def writejob(line):
    logger.Logger.log_info(line)
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

        elif line[1] == "twitter-hashtag":
            filename += "twitter-hashtag-{arg}"
            scraper = snscrape.modules.twitter.TwitterHashtagScraper(line[2])

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

        if not os.path.exists(filename):
            with open(filename, "w") as f:
                items = list(scraper.get_items())
                for count, each_item in enumerate(items):
                    url = check_filter(str(each_item))

                    if url and validators.url(url):
                        # logger.Logger.log_info("At item " + str(count) + " " + url)
                        f.write(url + "\n")

        logger.Logger.log_info("Done with " + filename)

    logger.Logger.log_info("Done")

if __name__ == "__main__":
    main()
