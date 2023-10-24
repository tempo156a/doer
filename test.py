import os
import feedparser
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

rss_url = os.environ.get(
    "RSS_URL",
    "https://www.upwork.com/ab/feed/jobs/rss?sort=recency&paging=0%3B500&api_params=1&q=&securityToken=2697f1a5e3f16ab5c96e0f61207881c2cbd08f9f5a00fbafc5980a42151c69a7811965b0c697e3f6a84726fcf8257c85aac057e958b9d090b18eed45f2889d5a&userUid=1294909912959053824&orgUid=1294909912959053826&ptc=1390780894369423360%2C1390780624317243392",
)

feed = feedparser.parse(rss_url)
total = len(feed.entries)
tqdm.write(f"Total: {total}")
progress = tqdm(total=total)
# for entry in feed.entries:
#     resp = requests.post(
#         "https://script.google.com/macros/s/AKfycbx7CzrFXxwG2iQ8xp8qpsOo6d4xRhjN87dg_BSmqa-g2UIQN6ctp-MJbwVCP-fjlgYw/exec",
#         json={
#             "method": "POST",
#             "sheet": "Sheet1",
#             "key": "Astrongpassword@123!!",
#             "payload": {
#                 "title": entry.title,
#                 "link": entry.link,
#                 "summary": entry.summary,
#                 "description": entry.description,
#                 "published": entry.published,
#             },
#         },
#         headers={"Content-Type": "application/json"},
#     )
#     if resp.status_code == 200:
#         print(f"Success: {entry.title}")
#     else:
#         print(f"Failed: {entry.title}")

#     progress.update(1)

CHUNK_SIZE = 3
chunk = []

for entry in feed.entries:
    chunk.append(entry)

    if len(chunk) == CHUNK_SIZE:
        with ThreadPoolExecutor(max_workers=CHUNK_SIZE) as executor:
            for entry in chunk:
                executor.submit(
                    requests.post,
                    "https://script.google.com/macros/s/AKfycbx7CzrFXxwG2iQ8xp8qpsOo6d4xRhjN87dg_BSmqa-g2UIQN6ctp-MJbwVCP-fjlgYw/exec",
                    json={
                        "method": "POST",
                        "sheet": "Sheet1",
                        "key": "Astrongpassword@123!!",
                        "payload": {
                            "title": entry.title,
                            "link": entry.link,
                            "summary": entry.summary,
                            "description": entry.description,
                            "published": entry.published,
                        },
                    },
                    headers={"Content-Type": "application/json"},
                )
                progress.update(1)
        chunk = []

if chunk:
    with ThreadPoolExecutor(max_workers=len(chunk)) as executor:
        for entry in chunk:
            executor.submit(
                requests.post,
                "https://script.google.com/macros/s/AKfycbx7CzrFXxwG2iQ8xp8qpsOo6d4xRhjN87dg_BSmqa-g2UIQN6ctp-MJbwVCP-fjlgYw/exec",
                json={
                    "method": "POST",
                    "sheet": "Sheet1",
                    "key": "Astrongpassword@123!!",
                    "payload": {
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.summary,
                        "description": entry.description,
                        "published": entry.published,
                    },
                },
                headers={"Content-Type": "application/json"},
            )
            progress.update(1)
    chunk = []

progress.close()
