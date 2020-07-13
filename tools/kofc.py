import requests
import json

# count = 1
count = 5963
url = "https://www.kofc.org/kfsrv/rest/v1/service/{num}/councilByCouncilNumber.json"
end = False

with open("kofc.txt", "a") as f:
    while not end:
        try:
            try:
                r = requests.get(url.format(num=count)).json()
                if website := r.get("webSite"):
                    f.write(website.rstrip() + "\n")
                    print(website.rstrip())
                else:
                    print("No website", count)

            except json.decoder.JSONDecodeError:
                print("JSON error", count)
                pass

        except KeyboardInterrupt:
            break

        count += 1
