import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://ilyasturki.com/feed.xml"
README = "README.md"
COUNT = 4

# The site answers 403 to urllib's default User-Agent.
request = urllib.request.Request(FEED, headers={"User-Agent": "github-profile-journal"})
with urllib.request.urlopen(request, timeout=30) as response:
    channel = ET.parse(response).getroot().find("channel")

lines = []
for item in channel.findall("item")[:COUNT]:
    date = parsedate_to_datetime(item.findtext("pubDate"))
    title = item.findtext("title").strip()
    link = item.findtext("link").strip()
    lines.append(f"- {date:%b} {date.day} · [{title}]({link})")

readme = open(README, encoding="utf-8").read()
updated, found = re.subn(
    r"(<!-- journal:start -->\n).*?(<!-- journal:end -->)",
    lambda m: m[1] + "\n".join(lines) + "\n" + m[2],
    readme,
    flags=re.S,
)
if not found:
    sys.exit("journal markers missing from README.md")
open(README, "w", encoding="utf-8").write(updated)
