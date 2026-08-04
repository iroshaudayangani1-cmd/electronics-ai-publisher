
import feedparser
import json
import re
import hashlib
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import os
from datetime import timezone
from bs4 import BeautifulSoup

from config.settings import NEWS_JSON


# ==========================================================
# ELECTRONICS RSS SOURCES
# ==========================================================

RSS_FEEDS = [

    {
        "name": "Hackaday",
        "url": "https://hackaday.com/blog/feed/",
        "trust": 10,
    },

    {
        "name": "All About Circuits",
        "url": "https://www.allaboutcircuits.com/rss/",
        "trust": 10,
    },

    {
        "name": "Arduino",
        "url": "https://blog.arduino.cc/feed/",
        "trust": 10,
    },

    {
        "name": "Raspberry Pi",
        "url": "https://www.raspberrypi.com/news/feed/",
        "trust": 10,
    },

    {
        "name": "Electronics Weekly",
        "url": "https://www.electronicsweekly.com/feed",
        "trust": 9,
    },

    {
        "name": "EE Times",
        "url": "https://www.eetimes.com/feed/",
        "trust": 9,
    },

    {
        "name": "Embedded Computing",
        "url": "https://embeddedcomputing.com/rss.xml",
        "trust": 9,
    },

    {
        "name": "IEEE Spectrum",
        "url": "https://spectrum.ieee.org/rss/fulltext",
        "trust": 10,
    },

]


# ==========================================================
# VIRAL KEYWORDS
# ==========================================================

KEYWORDS = {

    "arduino": 20,
    "esp32": 20,
    "raspberry pi": 20,
    "raspberry": 20,
    "robot": 18,
    "robotics": 18,
    "ai": 18,
    "artificial intelligence": 18,
    "embedded": 15,
    "microcontroller": 15,
    "microcontroller unit": 15,
    "iot": 15,
    "pcb": 15,
    "circuit": 15,
    "electronics": 10,
    "repair": 12,
    "fix": 12,
    "project": 20,
    "tutorial": 20,
    "guide": 18,
    "how to": 18,
    "battery": 10,
    "ev": 10,
    "sensor": 12,
    "semiconductor": 10,
    "chip": 10,
    "processor": 10,
    "open source": 15,
    "3d printing": 15,
}


# ==========================================================
# REMOVE HTML
# ==========================================================

def clean_html(text):

    if not text:
        return ""

    soup = BeautifulSoup(text, "html.parser")

    text = soup.get_text(" ", strip=True)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================================
# UNIQUE HASH
# ==========================================================

def article_hash(title):

    return hashlib.md5(
        title.lower().encode("utf-8")
    ).hexdigest()


# ==========================================================
# DATE PARSER
# ==========================================================

def parse_date(entry):

    if "published" not in entry:
        return None

    try:

        dt = parsedate_to_datetime(
            entry.published
        )

        if dt.tzinfo is None:

            dt = dt.replace(
                tzinfo=timezone.utc
            )

        return dt

    except Exception:

        return None
      # ==========================================================
# VIRAL SCORING
# ==========================================================

def calculate_score(article):

    score = 0

    text = (
        article["title"] + " " +
        article["summary"]
    ).lower()

    # ------------------------
    # Keyword score
    # ------------------------

    for keyword, value in KEYWORDS.items():

        if keyword in text:

            score += value

    # ------------------------
    # Trust score
    # ------------------------

    score += article["trust"]

    # ------------------------
    # Freshness score
    # ------------------------

    if article["published"]:

        age = datetime.now(
            timezone.utc
        ) - article["published"]

        hours = age.total_seconds() / 3600

        if hours <= 24:

            score += 20

        elif hours <= 48:

            score += 10

        elif hours <= 72:

            score += 5

        elif hours > 24 * 7:

            score -= 100

    # ------------------------
    # Image bonus
    # ------------------------

    if article["image"]:

        score += 5

    # ------------------------
    # Penalize unwanted content
    # ------------------------

    bad_words = [

        "advertisement",
        "advertising",
        "sponsored",
        "promotion",
        "press release",
        "buy now",
        "sale",

    ]

    for word in bad_words:

        if word in text:

            score -= 50

    return score


# ==========================================================
# IMAGE EXTRACTOR
# ==========================================================

def extract_image(entry):

    try:

        if "media_content" in entry:

            return entry.media_content[0]["url"]

    except Exception:

        pass

    try:

        if "media_thumbnail" in entry:

            return entry.media_thumbnail[0]["url"]

    except Exception:

        pass

    try:

        if "links" in entry:

            for link in entry.links:

                if link.get("type", "").startswith("image"):

                    return link.get("href")

    except Exception:

        pass

    return None


# ==========================================================
# DUPLICATE FILTER
# ==========================================================

def remove_duplicates(articles):

    seen = set()

    unique = []

    for article in articles:

        h = article_hash(article["title"])

        if h in seen:

            continue

        seen.add(h)

        unique.append(article)

    return unique
  # ==========================================================
# MAIN COLLECTOR
# ==========================================================

def collect_news():

    all_articles = []

    print("Collecting electronics articles...\n")

    for feed in RSS_FEEDS:

        print(f"Reading: {feed['name']}")

        try:

            rss = feedparser.parse(feed["url"])

            for entry in rss.entries:

                title = clean_html(
                    entry.get("title", "")
                )

                summary = clean_html(
                    entry.get("summary", "")
                )

                published = parse_date(entry)

                article = {

                    "title": title,

                    "summary": summary,

                    "source": feed["name"],

                    "url": entry.get("link", ""),

                    "published": published,

                    "image": extract_image(entry),

                    "trust": feed["trust"],

                }

                article["score"] = calculate_score(article)

                all_articles.append(article)

        except Exception as e:

            print(
                f"RSS failed: {feed['name']} -> {e}"
            )

    # ----------------------------------------

    # Remove duplicates

    # ----------------------------------------

    all_articles = remove_duplicates(all_articles)

    # ----------------------------------------

    # Remove old articles

    # ----------------------------------------

    filtered = []

    for article in all_articles:

        if article["score"] < 0:
            continue

        filtered.append(article)

    # ----------------------------------------

    # Sort by viral score

    # ----------------------------------------

    filtered.sort(

        key=lambda x: x["score"],

        reverse=True,

    )

    # ----------------------------------------

    # Keep ONLY Top 5

    # ----------------------------------------

    top5 = filtered[:5]

    print("\n===============================")
    print("TOP 5 ARTICLES")
    print("===============================")

    for i, item in enumerate(top5, start=1):

        print(
            f"[{item['score']}] {item['title']}"
        )

    # ----------------------------------------

    # Convert datetime to string

    # ----------------------------------------

    export = []

    for article in top5:

        a = article.copy()

        if a["published"]:

            a["published"] = (
                a["published"]
                .astimezone(timezone.utc)
                .isoformat()
            )

        export.append(a)

    os.makedirs("output/news", exist_ok=True)

    with open(

        NEWS_JSON,

        "w",

        encoding="utf-8",

    ) as f:

        json.dump(

            {

                "count": len(export),

                "articles": export,

            },

            f,

            indent=4,

            ensure_ascii=False,

        )

    print(
        f"\nSaved {len(export)} articles."
    )


if __name__ == "__main__":

    collect_news()
