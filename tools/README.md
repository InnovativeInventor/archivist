## Manual/Tools

This folder houses all of the manual jobs that I've done.

snscrape-job.sh runs local snscrape-jobs and packages them nicely for eventual upload to queuebot (creates jobs.txt, gives a nice filename, etc.)

filter-police.py was a simple script to help me filter out police/municipal twitter accounts out to prioritize them.

Notes:
Useful vim commands:
```
g!/.pdf/d
g!/./d
```

## Bookmarklet
Run server by calling:
```bash
uvicorn check:app
```

```
<a href="javascript:window.location="http://127.0.0.1:8000?url="+encodeURIComponent(document.location)">Add to Archive</a>
```

<a href="javascript:window.location="http://127.0.0.1:8000?url="+encodeURIComponent(document.location)">Add to Archive</a>
