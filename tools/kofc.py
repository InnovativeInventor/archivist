import json

import requests

## Finding all kofc websites
# count = 5963
# url = "https://www.kofc.org/kfsrv/rest/v1/service/{num}/councilByCouncilNumber.json"
# end = False

# with open("kofc.txt", "a") as f:
#     while not end:
#         try:
#             try:
#                 r = requests.get(url.format(num=count)).json()
#                 if website := r.get("webSite"):
#                     f.write(website.rstrip() + "\n")
#                     print(website.rstrip())
#                 else:
#                     print("No website", count)

#             except json.decoder.JSONDecodeError:
#                 print("JSON error", count)
#                 pass

#         except KeyboardInterrupt:
#             break

#         count += 1

## Finding all kofc websites on uknight
count = 17304
url = "http://uknight.org/CouncilSite/?CNO={num}"
reference_url = "http://uknight.org/CouncilSite/?CNO=0"
other_reference_url = "http://uknight.org/CouncilSite/?CNO=1"
end = False

nothing = requests.get(reference_url).content
null = requests.get(other_reference_url).content

with open("uknight.txt", "a") as f:
    while not end:
        try:
            r = requests.get(url.format(num=count))
            if r.content != nothing and r.content != null:
                f.write(url.format(num=count) + "\n")
                print("Website")
            else:
                print("No website", count, r.status_code)


        except KeyboardInterrupt:
            break

        count += 1
