import requests
import bs4
from datetime import datetime
import pytz

search_words = [ "bevq","bevco"]
hit_words = ["bevq","bev q"]

def get_search_results(searchInput,hit_words):
    r = requests.get("https://play.google.com/store/search?q="+searchInput+"&c=apps")
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    anchors = soup.findAll("a")
    detected_urls = []
    for anchor in anchors:
        try:
          url = anchor.attrs["href"]
          if "/store/apps/details" in url:
            divs = anchor.findAll("div")
            for div in divs:
              title = div.attrs["title"].lower()
              if any(hit in title for hit in hit_words):
                detected_urls.append(url)
        except KeyError:
            continue
    return detected_urls

status = False
for searches in search_words:
  hits = get_search_results(searches,hit_words)
  for hit in hits:
    status = True
    print("https://play.google.com"+hit)

if not status:
  print("BevQ not found as of : "+ str(datetime.now(pytz.timezone('Asia/Kolkata'))))
