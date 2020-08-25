## Archivist
Note: This project was rather quickly put together and started off as a bunch of separate scripts. As a result, it isn't particularly well organized since it has been adapted significantly to suit my archiving needs.

This project is for [queuebot](https://github.com/InnovativeInventor/queuebot) to archive deduplicated social media posts from culturally and politcally important accounts.

Currently there is a strong focus on governmental and activist tweets, but some Facebook accounts are also present. Deduplication is currently accomplished through a large bloom filter, which allows for space-efficient checking against previously archived tweets.

More documentation is forthcoming.


## Sync (with Internet Archive)
```bash
ia download --search 'collection:archivebot' --glob '*twitter-*.txt' -i -C --no-directories 
```
