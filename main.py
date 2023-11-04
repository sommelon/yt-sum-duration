import datetime
import os
from urllib.parse import parse_qs, urlparse
from pyyoutube import Api


def get_id_from_url(url):
    query = parse_qs(urlparse(url).query)
    return query.get("v", [None])[0]


def get_chunks(list_, size):
    chunks = [list_[i : i + size] for i in range(0, len(list_), size)]
    return chunks


with open("urls.lst") as f:
    urls = f.read().splitlines()
ids = []
for url in urls:
    id = get_id_from_url(url)
    if id:
        ids.append(id)
chunked_ids = get_chunks(ids, 20)  # so the url doesn't get truncated

api = Api(api_key=os.getenv("API_KEY"))
duration = 0
for ids in chunked_ids:
    response = api.get_video_by_id(video_id=ids)
    for item in response.items:
        duration += item.contentDetails.get_video_seconds_duration()


print(f"DURATION: {datetime.timedelta(seconds=duration)}")
