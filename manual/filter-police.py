import re

filters = ["police", "pd", "city", "town", "dmv", "chief", "rep", "fire", "fd", "SCDPS_PIO", "sheriff", "jail", "umass", "DOT", "fema", "ems", "patrol"]

with open("police-snscrape-raw.txt") as f:
    for each_line in f:
        if each_line:
            each_line = each_line.rstrip()
            line = re.sub(r'\+snscrape twitter-user', 'bash snscrape-job.sh', each_line)

            matches=False
            for each_filter in filters:
                if each_filter.lower() in each_line.lower():
                    matches = True
                    break

            if matches:
                print(line)
