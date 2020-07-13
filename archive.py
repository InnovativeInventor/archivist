import subprocess
import datetime
import sys
import logger

if __name__ == "__main__":
    p = subprocess.Popen(["go", "run", "deduplicate.go"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for count, line in enumerate(sys.stdin):
            if line := line.rstrip().split():
                filename = "jobs/"

                if line[1] == "twitter-user":
                    filename += "twitter-@{arg}"
                elif line[1] == "facebook-user":
                    filename += "facebook-@{arg}"
                elif line[1] == "facebook-group":
                    filename += "facebook-group-{arg}"
                elif line[1] == "twitter-list":
                    filename += "twitter-list-{arg}"
                else:
                    continue

                filename = filename.format(arg=line[2])
                filename += "-" + datetime.datetime.today().strftime('%Y%m%d')
                filename += ".txt"

                logger.Logger.log_info("Job " + filename)
                snscrape = subprocess.run(line, capture_output=True)

                for count, each_item in enumerate(snscrape.stdout.decode()):
                    result = p.stdin.write(each_item.encode())
                    result = p.stdout.readline()
                    log = p.stderr.readline()
                    logger.Logger.log_info("At item " + str(count))
                    print(result)
                    logger.Logger.log_info(log)

                break
    except KeyboardInterrupt:
        pass

    logger.Logger.log_info("Done")
    p.stdin.close()

