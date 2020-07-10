echo "snscrape twitter-user $1 > twitter-@$1-filtered.txt"
snscrape twitter-user $1 > twitter-@$1-filtered.txt

echo "https://archive.max.fan/twitter-@$1-filtered.txt" >> jobs.txt
