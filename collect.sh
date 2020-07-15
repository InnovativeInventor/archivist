python3 gather_accounts.py snscrape >> snscrape.txt

sort -u snscrape.txt > snscrape-temp.txt
mv snscrape-temp.txt snscrape.txt

python3 archive.py

#go run deduplicate.go | sort -u | python3 jobsplit.py

## Categories
# gov
#python3 archive.py TwitterGov socialbot >> socialbot.txt
#python3 archive.py UN socialbot >> socialbot.txt
#python3 archive.py BulgariaUNHCR socialbot >> socialbot.txt

# media
#python3 archive.py AP socialbot >> socialbot.txt
#python3 archive.py nytimes socialbot >> socialbot.txt
#python3 archive.py FiveThirtyEight socialbot >> socialbot.txt

# politcs
#python3 archive.py gop socialbot >> socialbot.txt
## note: DNC does not have a list

# other (optional)
#python3 archive.py parsely socialbot >> socialbot.txt # contains lists of lists of various notable people
#python3 archive.py pewresearch socialbot >> socialbot.txt 
#python3 archive.py techcrunch socialbot >> socialbot.txt 

#python3 archive.py socialbot >> socialbot.txt
## Sorting
#sort -u socialbot.txt > socialbot-temp.txt
#cat socialbot-temp.txt > socialbot.txt

#rm socialbot-temp.txt
